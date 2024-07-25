from artiq.experiment import *
from artiq.coredevice.sampler import adc_mu_to_volt
import numpy as np

class Sampler_Fast(EnvExperiment):
	kernel_invariants = {"Rate", "Period", "Duration", "nSamples", "nChannels", "Channels", "Names"}

	def build(self):
		self.setattr_device("core")
		self.setattr_device("sampler0")

	def prepare(self):
		self.Rate      = 1.E3			## [Hz]
		self.Period    = 1./self.Rate	## [s]
		self.Duration  = 5000.*ms			## [s]
		self.nSamples  = int(self.Rate*self.Duration) + 1 ## Can be even or odd
		self.nChannels = 2				## Number of channels to acquire (must be even)
		self.Channels  = [7, 6, 5, 4, 3, 2, 1, 0] ## Channel numbers in order of acquisition
		self.Gains     = [0, 0, 0, 0, 0, 0, 0, 0] ## Gains (G=0,1,2,3) for each channel
		self.Names     = ['Data_ch' + str(self.Channels[ch]) for ch in reversed(range(self.nChannels))]
		self.Data_mu   = np.zeros((self.nSamples, self.nChannels), dtype=np.int32)

		## Datasets must be scalars (bool, int, float or NumPy scalar) or NumPy arrays.
		self.set_dataset('Rate', self.Rate)
		self.set_dataset('Duration', self.Duration)
		self.set_dataset('nSamples', self.nSamples)
		self.set_dataset('Channels', self.Channels)
		self.set_dataset('Gains', self.Gains)

	@kernel
	def Initialize_Sampler(self):
		self.core.break_realtime()
		self.sampler0.init()
		for ch in range(8):
			self.sampler0.set_gain_mu(self.Channels[ch], self.Gains[ch])
		delay(1*ms)

	@kernel
	def Acquire_Samples(self):
		for i in range(self.nSamples):
			with parallel:
				self.sampler0.sample_mu(self.Data_mu[i])
				delay(self.Period)

	@kernel
	def Store_Samples(self):
		for ch in range(self.nChannels):
			Data_V = [adc_mu_to_volt(self.Data_mu[i,ch], self.Gains[ch]) for i in range(self.nSamples)]
			self.set_dataset(self.Names[ch], Data_V, broadcast=False, persist=False, archive=True)

	@kernel
	def run(self):
		self.core.reset()
		self.Initialize_Sampler()
		self.Acquire_Samples()
		self.Store_Samples()

		print('Channels =', [self.Channels[ch] for ch in range(self.nChannels)])
		print('Rate     =', self.Rate)
		print('nSamples =', self.nSamples)

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()
