from artiq.experiment import *


class CollisionErrorSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        self.core.reset()

        # With ttl1 generate two 4-ns long pulses separated with 1-ns delay.

        # SOLUTION -------------------------------------------------------------

        self.ttl1.pulse(4*ns)
        delay(1*ns)
        self.ttl1.pulse(4*ns)

        # END SOLUTION ---------------------------------------------------------