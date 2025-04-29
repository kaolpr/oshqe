from artiq.experiment import *


class Sed1Solution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        # Reset our system after previous experiment
        self.core.reset()

        # Set software (now) counter in the future
        self.core.break_realtime()

        state = False
        for i in range(2):
            state = not state
            self.ttl1.set_o(state)
            delay(10*ns)

