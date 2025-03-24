from artiq.experiment import *


class CCB(EnvExperiment):
    """CCB"""
    def build(self):
        self.setattr_device("ccb")

    def run(self):
        self.ccb.issue("create_applet", "Parabola via CCB",
           "${artiq_applet}plot_xy parabola.new")