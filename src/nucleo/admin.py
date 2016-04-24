'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from random import random
from . import Proceso

class Prioridad(object):
	
	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self.actual = 0
	
	def agregarProcesos(self, momento):
		if len(self.procesos) < 5 or random() < 0.25:
			proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], momento)
			self.procesos.append(proceso)
			return proceso
		return None
		
		
	def administrarProcesos(self, momento):
		proceso = None
		menor = 20
		for p in self.procesos:
			if not p.estado == "terminado":
				menor = min(menor, p.prioridad)
		for p in self.procesos:
			if menor < p.prioridad and p.estado == "ejecutando":
				p.estado = "listo" # tenia doble igual
			estados = [p1.estado for p1 in self.procesos]
			if menor == p.prioridad and p.estado == "listo" and not "ejecutando" in estados:
				p.iniciar(momento)
				break
		for p in self.procesos:
			if p.estado == "ejecutando":
				p.ejecutar()
				if p.rafaga < 0:
					p.finalizar(momento)
					proceso = self.procesos.index(p)
			else:
				if not p.prioridad == 1:
					p.envejecer()
				if p.edad <= 0 and p.prioridad > 1:
					p.priorizar()
		return proceso
	
	def __len__(self):
		return len(self.procesos)
	
	def __getitem__(self, i):
		return self.procesos[i]
