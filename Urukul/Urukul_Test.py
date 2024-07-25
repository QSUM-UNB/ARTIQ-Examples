from artiq.experiment import *

class Urukul_Test(EnvExperiment):
	"""DDS test"""

	def build(self):
		self.setattr_device("core")
		self.dds0 = self.get_device("urukul0_ch0")
		self.dds1 = self.get_device("urukul0_ch1")
		# self.dds2 = self.get_device("ad9914dds2")
		self.setattr_device("ttl4")
		# self.setattr_device("ttl1")
		# self.setattr_device("ttl2")
		# self.setattr_device("led0")

	@kernel
	def run(self):
		self.core.reset()
		self.ttl4.output()
		self.dds0.init()
		self.dds1.init()

		delay(1*ms)
		self.dds0.set_att(12.)
		self.dds1.set_att(12.)
		self.dds0.set(50*MHz, 0.0, 1.)
		self.dds1.set(50*MHz, 0.5, 1.)

		delay(1*ms)
		with parallel:
			self.ttl4.pulse(0.1*us)
			self.dds0.sw.on()
			self.dds1.sw.on()
		delay(1*us)
		with parallel:
			self.dds0.sw.off()
			self.dds1.sw.off()
			self.ttl4.pulse(0.1*us)

		# self.dds0.set(20*MHz)
		# self.dds2.set(200*MHz)
		# delay(1*us)

		# for i in range(10000):
		#     if i & 0x200:
		#         self.led.on()
		#     else:
		#         self.led.off()
		#     with parallel:
		#         with sequential:
		#             self.dds0.set(100*MHz + 4*i*kHz)
		#             self.ttl0.pulse(500*us)
		#             self.ttl1.pulse(500*us)
		#         self.ttl2.pulse(100*us)
		# self.led.off()
