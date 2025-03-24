from artiq.experiment import *
import numpy as np
import time

class Parabola(EnvExperiment):
    """Parabola"""

    def run(self):
        self.set_dataset("parabola", np.full(10, np.nan), persist=True)
        for i in range(10):
            self.mutate_dataset("parabola", i, i*i)
            time.sleep(0.5)

    def analyze(self):
        pass
