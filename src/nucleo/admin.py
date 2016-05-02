'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from random import random
from . import Proceso

class RoundRobin(object):
	
	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self.actual = 0
		self.quantum = 3
		self.q = 0
		self._inicializar()
	
	def _inicializar(self):
		for i in range(5):
			proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], 0.0)
			self.procesos.append(proceso)
	
	def agregarProcesos(self, momento):
		if random() < 0.2:
			proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], momento)
			self.procesos.append(proceso)
			return proceso
		return None
		
	def administrarProcesos(self, momento, bloqueo):
		proceso = None
		for p in self.procesos:
			if p.bloqueado():
				p.alistar()
				break
			
		for p in self.procesos:
			if bloqueo and p.ejecutando():
				p.bloquear()
				self.actual += 1
				self.q = 0
				break
		
		estados = [p1.estado for p1 in self.procesos]
		i = self.actual % len(self.procesos)
		if self.procesos:
			if self.procesos[i].terminado():
				self.actual += 1
			if self.procesos[i].listo() and not "ejecutando" in estados:
				self.procesos[i].iniciar(momento)
			if self.procesos[i].ejecutando():
				if self.q < self.quantum:
					self.procesos[i].ejecutar()
					self.q += 1
					if self.procesos[i].rafaga < 0:
						self.procesos[i].finalizar(momento)
						self.actual += 1
						self.q = 0
						proceso = i
				else:
					self.procesos[i].alistar()
					self.actual += 1
					self.q = 0					
		return proceso
	
	def __len__(self):
		return len(self.procesos)
	
	def __getitem__(self, i):
		return self.procesos[i]

