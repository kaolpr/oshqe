from artiq.experiment import *
from time import sleep


class Stages(EnvExperiment):
    """Exploring experiment run phases."""

    def build(self):    
        print("build")

    def prepare(self):
        print("prepare")

    def run(self):
        print("run")

    def analyze(self):
        print("analyze")
