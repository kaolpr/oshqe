import numpy as np
from artiq.coredevice.sampler import adc_mu_to_volt
from artiq.experiment import *

N_SAMPLER_CHANNELS = 2
N_SAMPLE_SETS = 200
DT_US = 8 * us  # sampling interval
# 100 samples * 8 us = 800 us


def map_gain(gain):
    gain = int(gain)
    if gain == 1:
        return 0
    elif gain == 10:
        return 1
    elif gain == 100:
        return 2
    elif gain == 1000:
        return 3
    else:
        raise ValueError("Invalid gain value: {}".format(gain))


class SamplerWaveformSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.ttl1 = self.get_device("ttl1")
        self.sampler = self.get_device("sampler0")

        self.setattr_argument(
            "gain", EnumerationValue(["1", "10", "100", "1000"], default="1")
        )

    def prepare(self):
        self.samples_mu = [0 for n in range(N_SAMPLE_SETS)]
        self.gain_modifier = map_gain(self.gain)

    @kernel
    def init(self):
        self.core.reset()
        self.core.break_realtime()

        self.ttl1.output()
        delay(1 * us)

        self.sampler.init()
        delay(1 * us)
        for ch in range(8):
            self.sampler.set_gain_mu(ch, self.gain_modifier)
            delay(1 * us)

    @kernel
    def run(self):
        # Reset our system after previous experiment, set SYSTEM time marker
        # in the future and ensure that our TTL channels are configured as inputs
        # and outputs
        self.init()

        # t0 will be our LOCAL time marker. For now it points the same point in
        # timeline as SYSTEM: now marker
        delay(1 * ms)
        t0 = now_mu()
        # ----------------------------------------------------------------------
        # Prepare timestamps for sampling
        timestamps = [
            t0 + self.core.seconds_to_mu(i * DT_US) for i in range(N_SAMPLE_SETS)
        ]

        # Temporary list to store sampled values
        smp = [0] * N_SAMPLER_CHANNELS
        for i in range(N_SAMPLE_SETS):
            at_mu(timestamps[i])
            self.sampler.sample_mu(smp)
            self.samples_mu[i] = smp[1]  # IN7

        # After the sampling is done, create and set the dataset with the sampled
        # values. In case the dataset was mutated in the time-critical section,
        # we would either need long delays to compensate for the fact that the
        # mutation is a RPC, or we would need to submit asynchronous RPCs.
        self.set_dataset("waveform.mu", self.samples_mu, persist=True)
        # ----------------------------------------------------------------------

    def analyze(self):
        waveform_mu = self.get_dataset("waveform.mu")
        # Convert the waveform from ADC units to volts
        waveform_voltage = [
            adc_mu_to_volt(sample, self.gain_modifier) for sample in waveform_mu
        ]

        # Calculate the DC component of the waveform
        dc = np.mean(waveform_voltage)

        # Set the dataset with the waveform voltage and DC component
        self.set_dataset("waveform.voltage", waveform_voltage, persist=True)
        self.set_dataset("waveform.dc", dc, persist=True)
