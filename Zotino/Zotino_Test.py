from artiq.experiment import *

class Zotino_Test(EnvExperiment):
	"""Test experiment for Zotino ADC: full-scale swing, rise/fall time, onset delay, update delay, etc."""

	def build(self):
		self.setattr_device("core")
		self.setattr_device("ttl4")
		self.dac = self.get_device("zotino0")

	def prepare(self):
		# self.channels = [0, 31] ## Ch: 0 - 31
		# self.voltages = [1., 1.]
		# self.zeros = [0., 0.]

		self.channels = [ch for ch in range(32)] ## Ch: 0 - 31
		self.zeros = [0. for _ in range(32)]
		self.volts = [
			0., 0., 0., 0., 9.999, 0., 0., 0.,
			0., 0., 0., 0., 0., 0., 0., 0.,
			0., 0., 0., 0., 0., 0., 0., 0.,
			0., 0., 0., 0., 0., 0., 0., 0.]

		self.tau_us = 1000.*us

	@kernel
	def run(self):
		self.core.reset()
		self.ttl4.output()
		self.dac.init()

		self.core.break_realtime()

		# 8-bit word sets the color of the user LEDs on the DAC
		# MSB = LED 7, LSB = LED 0
		self.dac.set_leds(0b00000000) #1 = on; 0 = off
		delay(10*us)

		self.dac.set_dac(self.zeros[0:8], self.channels[0:8])
		delay(40*us)
		self.dac.set_dac(self.zeros[8:16], self.channels[8:16])
		delay(40*us)
		self.dac.set_dac(self.zeros[16:24], self.channels[16:24])
		delay(40*us)
		self.dac.set_dac(self.zeros[24:32], self.channels[24:32])

		while(True):
			delay(100*us)

			with parallel:
				self.ttl4.pulse(self.tau_us)
				with sequential:
					self.dac.set_dac([self.volts[4]], [4])
					delay(0.5*self.tau_us)
					self.dac.set_dac([0.], [4])


if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()