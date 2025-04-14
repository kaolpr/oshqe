from artiq.experiment import *
import numpy as np

N_SAMPLER_CHANNELS = 2
PERIOD_US = 28 * us
N_SAMPLES = 2


class SamplerTimesSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.ttl1 = self.get_device("ttl1")

        self.sampler = self.get_device("sampler0")

    @kernel
    def init(self):
        self.core.reset()
        self.core.break_realtime()

        self.ttl1.output()
        delay(1 * us)

        self.sampler.init()
        delay(1 * us)
        for ch in range(8):
            self.sampler.set_gain_mu(ch, 0)
            delay(1 * us)

    @kernel
    def generate_pulses(self):
        # The loop below generates a 'square' wave on TTL1 output channel.
        # Genrated wave has period of PERIOD_US and lasts for
        # N_SAMPLES * PERIOD_US
        for _ in range(N_SAMPLES):
            self.ttl1.pulse(PERIOD_US / 2)
            delay(PERIOD_US / 2)

    def prepare(self):
        self.voltages = [0.0 for n in range(2 * N_SAMPLES)]
        self.sampled_values = [[0.0] * N_SAMPLER_CHANNELS for _ in range(2 * N_SAMPLES)]

        # A list containing timestamps of sampled values.
        self.timestamps = [np.int64(0) for n in range(2 * N_SAMPLES + 1)]

    @kernel
    def run(self):
        # Reset our system after previous experiment, set SYSTEM time marker
        # in the future and ensure that our TTL channels are configured as inputs
        # and outputs
        self.init()

        # t0 will be our LOCAL time marker. For now it points the same point in
        # timeline as SYSTEM: now marker
        t0 = now_mu()
        # Generate pulses on TTL1 output channel
        self.generate_pulses()
        # Set system time pointer back to t0
        at_mu(t0)

        # ----------------------------------------------------------------------
        # Since we want to sample each state (both on and off) we need to sample
        # signal twice during one period.
        self.timestamps[0] = t0
        delay(PERIOD_US / 4)
        for i in range(2 * N_SAMPLES):
            self.timestamps[i + 1] = now_mu()
            self.sampler.sample(self.sampled_values[i])
            delay(PERIOD_US / 2)
        # ----------------------------------------------------------------------

    def analyze(self):
        # Now we calculate the difference between consecutive timestamps...
        dts = [
            self.core.mu_to_seconds(self.timestamps[i + 1] - self.timestamps[i])
            for i in range(2 * N_SAMPLES)
        ]
        # ... and convert them to microseconds
        dts_us = [dt * 1e6 for dt in dts]

        # This represents the expected timeline of sampled values.
        expected_timeline = [
            (PERIOD_US / 4 + i * PERIOD_US / 2) * 1e6 for i in range(2 * N_SAMPLES)
        ]

        actual = []
        for i, dt in enumerate(dts_us):
            if i == 0:
                actual.append(dt)
            else:
                actual.append(actual[i - 1] + dt)

        # Now retrieve sampled values and place them in a list
        self.voltages = [sample[1] for sample in self.sampled_values]

        print("Timestamps_difference: ", dts_us)
        print("Expected\tActual\t\tVoltage")
        for et, ts, v in zip(expected_timeline, actual, self.voltages):
            print(f"{et:.2f} us\t{ts:.2f} us\t{v:.2f} V")
