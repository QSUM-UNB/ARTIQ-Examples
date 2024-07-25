from artiq.experiment import *

#This code demonstrates how to use a TTL pulse (ttl0) to trigger another event.
#In this code the event being triggered is another ttl pulse.
#The same principle can be used to trigger an experimental sequence.

#TTL pulses occur 5.158 us appart with about 1 ns jitter

class TTL_Trigger(EnvExperiment):
	"""TTL Input Edge as Trigger"""
	def build(self): 							#Adds the device drivers as attributes and adds the keys to the kernel invarients     
		self.setattr_device("core")             #sets drivers of core device as attributes
		self.setattr_device("ttl0")
		self.setattr_device("ttl4")
		
	@kernel
	def run(self):                              
		self.core.reset()						#resets core device		
		self.ttl0.input()						#sets TTL0 as an input
		self.ttl4.output()						#sets TTL4 as an output
		
		delay(1*us)								#1 us delay, necessary for using trigger. collision error reported if removed
		
		t_end = self.ttl0.gate_rising(0.5*ms)	#opens gate window for rising edges to be detected on TTL0
												#sets variable t_end as time (in MUs) at which detection stops
												
		t_edge = self.ttl0.timestamp_mu(t_end)	#sets variable t_edge as time (in MUs) at which first edge is detected
												#if no edge is detected, sets t_edge to -1

		if t_edge > 0:							#runs if an edge has been detected
			at_mu(t_edge)						#set time cursor to position of edge
			delay(5*us)							#delay to prevent underflow
			self.ttl4.pulse(1*ms)				#outputs pulse on TTL4
			print("Trigger detected")
		else:
			print("No trigger detected in gate window")

		# self.ttl0.count(t_end)					#discard remaining edges and close gate

if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()
