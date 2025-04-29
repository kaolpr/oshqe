from artiq.experiment import *


class RtioAnalyzerLog(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl1")
        self.test = [i for i in range(1000)]

    @kernel
    def run(self):
        self.core.reset()
        for i in range(1000):
            self.ttl1.pulse(.2*us)
            rtio_log("test_trace", "i", self.test)
            delay(.2*us)