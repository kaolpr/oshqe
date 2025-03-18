from artiq.experiment import *
import numpy as np
import time

class Parabola(EnvExperiment):
    """Parabola"""
    def build(self):
        pass  # no devices used

    def run(self):
        self.set_dataset("parabola", np.full(10, np.nan), broadcast=True)
        for i in range(10):
            self.mutate_dataset("parabola", i, i*i)
            time.sleep(0.5)

    def analyze(self):
        parabola = self.get_dataset("parabola")
        print(sum(parabola))