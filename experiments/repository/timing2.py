from artiq.experiment import *


class Timing2Solution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")
        self.setattr_device("ttl3")

    @kernel
    def run(self):
        # Reset our system after previous experiment
        self.core.reset()

        # Set software (now) counter in the future
        self.core.break_realtime()
        
        # SOLUTION



        # END SOLUTION

