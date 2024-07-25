from artiq.experiment import *
from artiq.coredevice.sampler import adc_mu_to_volt
import numpy as np

class Sampler_Fast_Trigger(EnvExperiment):
	kernel_invariants = {"Rate", "Period", "Duration", "nSamples", "nChannels", "Channels", "DataLabels", "GateWindow"}

	def build(self):
		self.setattr_device("core")
		self.setattr_device("sampler0")
		self.setattr_device("ttl0")

	def prepare(self):
		self.Rate       = 100.E3		## Sample rate [Hz]
		self.Period     = 1./self.Rate	## Sample period [s]
		self.Duration   = 1.*ms			## Sample duration [s]
		self.nSamples   = int(self.Rate*self.Duration) + 1 ## Number of samples per channel (can be even or odd)
		self.nChannels  = 2				## Number of channels to acquire (must be even)
		self.Channels   = [7, 6, 5, 4, 3, 2, 1, 0] ## Channel numbers in order of acquisition
		self.Gains      = [0, 0, 0, 0, 0, 0, 0, 0] ## Gains (G=0,1,2,3) for each channel
		self.DataLabels = ['Data_ch' + str(self.Channels[ch]) for ch in reversed(range(self.nChannels))]
		self.Data_mu    = np.zeros((self.nSamples, self.nChannels), dtype=np.int32)
		self.GateWindow = 100.*ms		## Gate window for rising edge trigger to be detected
		self.tEdge      = 0

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
		delay(1.*ms)

	@kernel
	def Acquire_Samples(self):
		for i in range(self.nSamples):
			with parallel:
				self.sampler0.sample_mu(self.Data_mu[i])
				delay(self.Period)

	@kernel
	def Trigger_Sampler(self) -> TInt64:
		tEnd  = self.ttl0.gate_rising(self.GateWindow) ## Time (in mu) at which edge detection stops.
		tEdge = self.ttl0.timestamp_mu(tEnd)	## Time (in mu) of first edge detection. If no edge is detected by tEnd, tEdge = -1.
		if tEdge > 0:
			at_mu(tEdge)						## Set time cursor to time of edge detection
			delay(10.*us)						## Delay to prevent RTIO Underflow
			self.Acquire_Samples()
			self.Store_Samples()
		
		return tEdge

	@kernel
	def Store_Samples(self):
		for ch in range(self.nChannels):
			Data_V = [adc_mu_to_volt(self.Data_mu[i,ch], self.Gains[ch]) for i in range(self.nSamples)]
			self.set_dataset(self.DataLabels[ch], Data_V, broadcast=False, persist=False, archive=True)

	@rpc(flags={"async"})
	def Print_Results(self, tEdge=-1):
		if tEdge > 0:
			print("Trigger detected.")
			print("tEdge    =", self.tEdge)
			print("Channels =", [self.Channels[ch] for ch in range(self.nChannels)])
			print("Rate     =", self.Rate)
			print("nSamples =", self.nSamples)
		else:
			print("No trigger detected in gate window =", self.GateWindow, 's')
		
	@kernel
	def run(self):
		self.core.reset()
		self.ttl0.input()
		self.Initialize_Sampler()
		tEdge = self.Trigger_Sampler()
		self.Print_Results(tEdge)

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()