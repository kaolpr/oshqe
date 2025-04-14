from artiq.experiment import *
from artiq.language.types import TFloat
from user import user_id
import numpy as np
from artiq.coredevice.sampler import adc_mu_to_volt

N_SAMPLER_CHANNELS = 2
N_SAMPLE_SETS = 200
DT_US = 8 * us
# 100 samples * 8 us = 800 us


def map_gain(gain):
    gain = int(gain)
    if gain == 1:
        return 0
    elif gain == 10:
        return 1
    elif gain == 100:
        return 2
    elif gain == 1000:
        return 3
    else:
        raise ValueError("Invalid gain value: {}".format(gain))


class SamplerWaveformSolution(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.ttl1 = self.get_device("ttl1")
        self.ttl3 = self.get_device("ttl3")
        self.ttls_out = [self.ttl1, self.ttl3]
        self.sampler = self.get_device("sampler0")

        self.setattr_argument("gain", EnumerationValue(["1", "10", "100", "1000"], default="1"))

        self.gain_modifier = map_gain(self.gain)


    def prepare(self):
        # 1 kHz - 1 ms
        # let's take 40 samples - every 25 us
        # self.set_dataset("sampler_waveform", np.full(N_SAMPLE_SETS, np.nan), persist=True)

        self.samples_mu = [0 for n in range(N_SAMPLE_SETS)]


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
            self.sampler.set_gain_mu(ch, self.gain_modifier)
            delay(1 * us)

    @kernel
    def run(self):
        # Reset our system after previous experiment, set SYSTEM time marker 
        # in the future and ensure that our TTL channels are configured as inputs
        # and outputs
        self.init()

        # t0 will be our LOCAL time marker. For now it points the same point in
        # timeline as SYSTEM: now marker
        delay(1*ms)
        t0 = now_mu()

        # Generate pulses on TTL1 output channel

        # ----------------------------------------------------------------------
        smp = [0] * N_SAMPLER_CHANNELS
        timestamps = [t0 + self.core.seconds_to_mu(i * DT_US) for i in range(N_SAMPLE_SETS)]
        for i in range(N_SAMPLE_SETS):
            at_mu(timestamps[i])
            self.sampler.sample_mu(smp)
            self.samples_mu[i] = smp[1] # IN7

        self.set_dataset("waveform.mu", self.samples_mu, persist=True)
        # ----------------------------------------------------------------------

    def analyze(self):
        waveform_mu = self.get_dataset("waveform.mu")
        waveform_voltage = [adc_mu_to_volt(sample, self.gain_modifier) for sample in waveform_mu]


        dc = np.mean(waveform_voltage)

        self.set_dataset("waveform.voltage", waveform_voltage, persist=True)
        self.set_dataset("waveform.dc", dc, persist=True)

