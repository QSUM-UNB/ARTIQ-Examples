from artiq.experiment import *

def print_underflow():
	print('RTIO underflow occurred.')

class Tutorial(EnvExperiment):
	def build(self):
		self.setattr_device('core')
		self.setattr_device('ttl4')
		self.setattr_device('ttl5')

	@kernel
	def run(self):
		self.core.reset()
		self.ttl4.output()
		self.ttl5.output()
		try:
			for _ in range(1000000):
				# with parallel:
				# 	self.ttl4.pulse(2*us)
				# 	self.ttl5.pulse(4*us)
				# delay(4*us)

				with parallel:
					with sequential:
						self.ttl4.pulse(2*us)
						delay(1*us)
						self.ttl4.pulse(1*us)
					self.ttl5.pulse(4*us)
				delay(4*us)

		except RTIOUnderflow:
			print_underflow()

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()