from artiq.experiment import *


class LED(EnvExperiment):
	def build(self):
		self.setattr_device("core")
		self.setattr_device("led0")
		self.setattr_device("led1")

	@kernel
	def sos(self):
	##	SOS signal on LED1:
		for _ in range(3):
			self.led1.pulse(250*ms)
			delay(750*ms)
		for _ in range(3):
			self.led1.pulse(750*ms)
			delay(250*ms)
		for _ in range(3):
			self.led1.pulse(250*ms)
			delay(750*ms)

	@kernel
	def run(self):
		self.core.reset()
		self.led0.off()

		for _ in range(3):
			self.sos()
			delay(1000*ms)


if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()
