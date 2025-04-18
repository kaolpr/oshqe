from artiq.experiment import *
from user import user_id
from common import Scope


class Timing4Solution(EnvExperiment):
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
        
        # SOLUTION -------------------------------------------------------------

        with parallel:
            self.ttl1.pulse(2*us)
            with sequential:
                self.ttl3.pulse(1*us)
                delay(2*us)
                self.ttl3.pulse(1*us)
        self.ttl1.pulse(1*us)

        # END SOLUTION ---------------------------------------------------------
