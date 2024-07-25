import numpy as np

from artiq.experiment import *
from scipy import signal

class ZotinoTest(EnvExperiment):
	"""Zotino triangle wave"""

	def build(self):
		self.setattr_device("core")
		self.dac = self.get_device("zotino0")
		self.setattr_device("ttl4")

	def prepare(self):
		self.channel = 0
		self.period  = 100.*ms
		self.n_samples = 512
		self.amp = 1.
		t = np.linspace(0, 1, self.n_samples)
		self.voltages = self.amp*signal.sawtooth(2*np.pi*t, 0.5)
		self.interval = self.period/self.n_samples

	@kernel
	def run(self):
		self.core.reset()
		self.ttl4.output()
		self.dac.init()

		delay(1*ms)

		# for _ in range(5):
		while True:
			with parallel:
				self.ttl4.pulse(self.period/2)
				for i in range(self.n_samples):
					self.dac.set_dac([self.voltages[i]], [self.channel])
					delay(self.interval)
		
		# self.dac.set_dac([0.], [self.channel])

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()