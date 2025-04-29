from artiq.experiment import *


class CollisionError(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        self.core.reset()

        # SOLUTION -------------------------------------------------------------

        # TODO Your code should be here

        # END SOLUTION ---------------------------------------------------------
