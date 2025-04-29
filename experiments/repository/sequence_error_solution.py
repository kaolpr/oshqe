from artiq.experiment import *


class SequenceErrorSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        self.core.reset()

        # Try to schedule n pulses from the last falling edge to the first rising
        # edge. Assume n pulses, each of 1 us duration and separated by 1 us.

        n = 2

        # SOLUTION -------------------------------------------------------------

        t_high_mu = self.core.seconds_to_mu(1 * us)
        t_low_mu = self.core.seconds_to_mu(1 * us)
        t_period_mu = t_high_mu + t_low_mu

        at_mu(now_mu() + n * t_period_mu)
        for _ in range(n):
            self.ttl1.off()
            delay_mu(-t_high_mu)
            self.ttl1.on()
            delay_mu(-t_low_mu)

        # END SOLUTION ---------------------------------------------------------
