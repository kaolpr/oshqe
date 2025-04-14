from artiq.experiment import *

N_SAMPLER_CHANNELS = 2
PERIOD_US = 28 * us
N_SAMPLES = 8


class SamplerBasicExcercise(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.ttl1 = self.get_device("ttl1")

        # ----------------------------------------------------------------------
        """
        TODO: Get the sampler device
        """
        # -----------------------------------------------------------------------

    @kernel
    def init(self):
        self.core.reset()
        self.core.break_realtime()

        self.ttl1.output()
        delay(1 * us)

        # ----------------------------------------------------------------------
        """
        TODO: Initialize the sampler device and set the gain for all channels
            to 1. Assume delay(1 * us) is needed after each command.
        """
        # -----------------------------------------------------------------------

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
        self.sampled_values_mu = [
            [0] * N_SAMPLER_CHANNELS for _ in range(2 * N_SAMPLES)
        ]

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
        """
        TODO: Place your code here

        Sample the signal from TTL1 using the sampler device. Signal should be
        sampled twice during one period. 

        Populate the self.sampled_values list with sampled values.
        """
        # ----------------------------------------------------------------------

    def analyze(self):
        # Now retrieve sampled values and place them in a final list
        self.voltages = [sample[0] for sample in self.sampled_values]
        print(self.voltages)
