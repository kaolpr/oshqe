from artiq.experiment import *


class RtioAnalyzer(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        self.core.reset()
        for i in range(1000):
            self.ttl1.pulse(.2*us)
            delay(.2*us)