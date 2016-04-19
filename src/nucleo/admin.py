'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from random import random
from . import Proceso

class FCFS(object):
	
	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self.cantProcesos = 0
	
	def agregarProcesos(self, momento):
		if self.cantProcesos < 5 or random() < 0.25:
			proceso = Proceso(self._PROCESOS[self.cantProcesos % len(self._PROCESOS)], momento)
			self.procesos.append(proceso)
			self.cantProcesos += 1
			return proceso
		return None
		
	def administrarProcesos(self, momento):
		proceso = None
		if self.procesos:
			if self.procesos[0].estado == "listo":
				self.procesos[0].iniciar(momento)
			if self.procesos[0].estado == "ejecutando":
				self.procesos[0].ejecutar()
				if self.procesos[0].rafaga < 0:
					self.procesos[0].finalizar(momento)
			if self.procesos[0].estado == "terminado":
				proceso = self.procesos.pop(0)
		return proceso
