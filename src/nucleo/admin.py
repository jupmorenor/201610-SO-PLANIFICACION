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
		self.actual = 0
	
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
			if self.procesos[self.actual].estado == "listo":
				self.procesos[self.actual].iniciar(momento)
			if self.procesos[self.actual].estado == "ejecutando":
				self.procesos[self.actual].ejecutar()
				if self.procesos[self.actual].rafaga < 0:
					self.procesos[self.actual].finalizar(momento)
			if self.procesos[self.actual].estado == "terminado":
				proceso = self.procesos.pop(self.actual)
		return proceso

class SJF(FCFS):
	
	def __init__(self):
		super(SJF, self).__init__()
	
	def administrarProcesos(self, momento):
		proceso = None
		menor = 20
		estados = [p.estado for p in self.procesos]
		for p in self.procesos:
			if not p.estado == "terminado":
				menor = min(menor, p.rafaga)
		for p in self.procesos:
			if "ejecutando" not in estados:
				if menor == p.rafaga and p.estado == "listo":
					p.iniciar(momento)
			if p.estado == "ejecutando":
				p.ejecutar()
				if p.rafaga < 0:
					p.finalizar(momento)
			if p.estado == "terminado":
				proceso = self.procesos.index(p)
		#proceso = self.procesos[i] if i is not None else i
		return proceso
		
		
class SRTF(SJF):
	
	def __init__(self):
		super(SRTF, self).__init__()


class RoundRobin(SRTF):
	
	def __init__(self):
		super(RoundRobin, self).__init__()
	
				