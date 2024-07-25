from artiq.experiment import *
from artiq.coredevice.sampler import adc_mu_to_volt
import numpy as np
import csv

class Sampler_SaveToFile(EnvExperiment):
	kernel_invariants = {"Rate", "Period", "Duration", "nSamples", "nChannels", "Channels", "Names"}

	def build(self):
		self.setattr_device("core")
		self.setattr_device("sampler0")

	def prepare(self):
		self.Rate      = 8.E3			## [Hz]
		self.Period    = 1./self.Rate	## [s]
		self.Duration  = 10.*ms			## [s]
		self.nSamples  = int(self.Rate*self.Duration) + 1 ## Can be even or odd
		self.nChannels = 2				## Number of channels to acquire (must be even)
		self.Channels  = [7, 6, 5, 4, 3, 2, 1, 0] ## Channel numbers in order of acquisition
		self.Gains     = [0, 1, 0, 0, 0, 0, 0, 0] ## Gains (G=0,1,2,3) for each channel
		self.Names     = ['Data_ch' + str(self.Channels[ch]) for ch in reversed(range(self.nChannels))]
		self.Buffer    = np.zeros((self.nChannels, self.nSamples), dtype=np.float32)

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

	@rpc(flags={"async"})
	def Write_Samples_To_Buffer(self, channel, index, value):
		self.Buffer[channel, index] = value

	@kernel
	def Acquire_Samples(self):
		temp = [0.]*self.nChannels
		for i in range(self.nSamples):
			with parallel:
				self.sampler0.sample(temp)
				delay(self.Period)
			for ch in range(self.nChannels):
				self.Write_Samples_To_Buffer(ch, i, temp[ch])

	@rpc(flags={"async"})
	def Write_Samples_To_Text(self):
		# Write the samples to a text file
		with open("Sampler//samples.txt", "w") as outfile:
			for ch in range(self.nChannels):
				outfile.write("ch{}\n".format(self.Channels[ch]))
				for sample in self.Buffer[ch]:
					outfile.write("{:.6E}\n".format(sample))

	@rpc(flags={"async"})
	def Write_Samples_To_CSV(self):
		# Write the samples to a text file
		with open('Sampler//test.csv', 'w', newline='\n') as file:
			writer = csv.writer(file)
			writer.writerow(['ch{}'.format(self.Channels[ch]) for ch in range(self.nChannels)])
			for i in range(self.nSamples):
				writer.writerow(self.Buffer[:,i])

	@kernel
	def run(self):
		self.core.reset()
		self.Initialize_Sampler()
		self.Acquire_Samples()
		# self.Write_Samples_To_Text()
		self.Write_Samples_To_CSV()

		# print('Channels =', [self.Channels[ch] for ch in range(self.nChannels)])
		# print('Rate     =', self.Rate)
		# print('nSamples =', self.nSamples)

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()
