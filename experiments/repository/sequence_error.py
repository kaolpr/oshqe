from artiq.experiment import *


class SequenceError(EnvExperiment):
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

        # TODO Your code should be here

        # END SOLUTION ---------------------------------------------------------
        