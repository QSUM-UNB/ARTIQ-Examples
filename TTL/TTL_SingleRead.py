from artiq.experiment import *

#This code takes a single read from TTL0 and prints the voltage 

class TTL_SingleRead(EnvExperiment):
	"""TTL Input Read"""

	def build(self):
		self.setattr_device("core")			#sets drivers for core device as attributes
		self.setattr_device("ttl0")
		self.setattr_device("ttl4")

	@kernel
	def run(self):                              
		self.core.reset()					#resets core device
		self.ttl0.input()					#sets TTL0 as an input
		self.ttl4.output()
		self.core.break_realtime()			#moves timestamp forward to prevent underflow
											#this can also be achieved with a fixed delay

		with parallel:
			self.ttl4.pulse(20*us)
			with sequential:
				delay(10*us)
				self.ttl0.sample_input()	#reads current value of TTL0

		input = self.ttl0.sample_get()		#stores value of TTL0 as input variable
		print(input)						#prints value of input variabled

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()
