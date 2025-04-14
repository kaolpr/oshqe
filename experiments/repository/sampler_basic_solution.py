from artiq.experiment import *
from user import user_id
from common import Scope
import numpy as np

N_SAMPLER_CHANNELS = 2
PERIOD_US = 28 * us
N_SAMPLES = 8


class SamplerBasicExcerciseSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.ttl1 = self.get_device("ttl1")
        self.ttl3 = self.get_device("ttl3")
        self.ttls_out = [self.ttl1, self.ttl3]
        

        # 
        self.sampler = self.get_device("sampler0")
        # 

    @kernel
    def init(self):
        self.core.reset()
        self.core.break_realtime()

        for ttl in self.ttls_out:
            ttl.output()
            delay(1 * us)

        # 
        self.sampler.init()
        delay(1 * us)
        for ch in range(8):
            self.sampler.set_gain_mu(ch, 0)
            delay(1 * us)


    @kernel
    def generate_pulses(self):

        # The loop below generates a 'square' wave on TTL1 output channel.
        # Genrated wave has period of PERIOD_US (30 * us) and lasts for
        # N_SAMPLES * PERIOD_US (240 * us)
        for _ in range(N_SAMPLES):
            self.ttl1.pulse(PERIOD_US / 2) 
            delay(PERIOD_US / 2)
        

    def prepare(self):
        # 
        self.voltages = [0.0 for n in range(2*N_SAMPLES)]
        self.sampled_values = [[0.0] * N_SAMPLER_CHANNELS for _ in range(2*N_SAMPLES)]
        self.sampled_values_mu = [[0] * N_SAMPLER_CHANNELS for _ in range(2*N_SAMPLES)]


    @kernel
    def run(self):
        # Reset our system after previous experiment, set SYSTEM time marker 
        # in the future and ensure that our TTL channels are configured as inputs
        # and outputs
        self.init()

        # t0 will be our LOCAL time marker. For now it points the same point in
        # timeline as SYSTEM: now marker
        t0 = now_mu()
        # Generate pulses on TTL1 output channel
        self.generate_pulses()
        # Set system time pointer back to t0
        at_mu(t0)

        # ----------------------------------------------------------------------      
        for i in range(2*N_SAMPLES):
            at_mu(t0 + self.core.seconds_to_mu(PERIOD_US/4 + i*PERIOD_US/2))
            self.sampler.sample(self.sampled_values[i])
        # ----------------------------------------------------------------------

    def analyze(self):
        # Now retrieve sampled values and place them in a list
        self.voltages = [sample[0] for sample in self.sampled_values]
        print(self.voltages)

        