import numpy as np
from artiq.coredevice.sampler import adc_mu_to_volt
from artiq.experiment import *

N_SAMPLER_CHANNELS = 2
N_SAMPLE_SETS = 200
DT_US = 8 * us  # sampling interval
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


class SamplerWaveform(EnvExperiment):
    def build(self):
        # ----------------------------------------------------------------------
        """
        TODO: Create all the devices needed for the experiment and object attributes
        """
        pass
        # ----------------------------------------------------------------------

    def prepare(self):
        # ----------------------------------------------------------------------
        """
        TODO: Create the list to store the sampled values
        """
        pass
        # ----------------------------------------------------------------------

    @kernel
    def init(self):
        self.core.reset()
        self.core.break_realtime()

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
        delay(1 * ms)
        t0 = now_mu()

        # ----------------------------------------------------------------------
        """
        TODO: Sample the waveform and store the sampled values in the list. 
            Create a dataset named "waveform.mu" to store the sampled values.
            HINT: You can create a list of timestamps before entering the loop.
        """
        # ----------------------------------------------------------------------

    def analyze(self):
        # ----------------------------------------------------------------------
        """
        TODO: Analyze the sampled waveform, calculate the DC component, and convert
            the waveform from machine units to volts. Store the results in datasets
            named "waveform.voltage" and "waveform.dc".

            HINT: Use the adc_mu_to_volt function to convert the waveform from ADC
            units to volts.
        """
        # ----------------------------------------------------------------------
        pass
