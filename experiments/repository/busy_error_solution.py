from artiq.experiment import *


class BusyErrorSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.urukul = self.get_device("urukul0_cpld")
        self.urukul_channels = [
            self.get_device(f"urukul0_ch0")
        ]
        self.setattr_device("ttl1")

    @kernel
    def run(self):
        self.core.reset()

        # Set Urukul channel attenuation to 0.0. Then try setting it to 5.0 dB.
        # Second operation should start 20 ns after the start of the first operation.

        # SOLUTION -------------------------------------------------------------

        nmu = now_mu()
        self.urukul_channels[0].set_att(0.0)
        at_mu(nmu)
        delay(20*ns)
        self.urukul_channels[0].set_att(5.0)

        # END SOLUTION ---------------------------------------------------------
