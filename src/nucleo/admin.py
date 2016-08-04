'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from random import random
from . import Proceso

class MulticolasRetro(object):
	
	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self.colaActual = 1
		self.actual = 0
		self.quantum1 = 3
		self.quantum2 = 5
		self.q = 0
		self._inicializar()
	
	def _inicializar(self):
		for i in range(5):
			proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], 0)
			self.procesos.append(proceso)
	
	def agregarProcesos(self, momento):
		if random() < 0.2:
			proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], momento)
			self.procesos.append(proceso)
			return proceso
		return None
		
	def administrarProcesos(self, momento, bloqueo):
		proceso = None
		menor = 20
		priors = [p2.prioridad for p2 in self.procesos]
		if 1 in priors:
			self.colaActual = 1
		elif 2 in priors:
			self.colaActual = 2
		else:
			self.colaActual = 3
			
		for p in self.procesos:
			if p.bloqueado():
				p.alistar()
				break
			
		for p in self.procesos:
			if bloqueo and p.ejecutando():
				p.bloquear()
				break
			
		for p in self.procesos:
			if not p.terminado():
				menor = min(menor, p.prioridad)
		
		for p in self.procesos:
			if not p.prioridad == 1:
				p.envejecer()
			if p.edad <= 0 and p.prioridad > 1:
				p.priorizar()
				
		if self.colaActual == 1:
			estados = [p1.estado for p1 in self.procesos]
			priors = [p2.prioridad for p2 in self.procesos]
			i = self.actual % len(self.procesos)
			if 1 in priors:
				while self.procesos[i].terminado() or self.procesos[i].prioridad != 1:
					self.actual += 1
					i+=1
				if self.procesos[i].listo() and not "ejecutando" in estados:
					self.procesos[i].iniciar(momento)
				if self.procesos[i].ejecutando():
					if self.q < self.quantum1:
						self.procesos[i].ejecutar()
						self.q += 1
						if self.procesos[i].rafaga < 0:
							self.procesos[i].finalizar(momento)
							self.actual += 1
							self.q = 0
							proceso = i
					else:
						self.procesos[i].alistar()
						self.procesos[i].degradar()
						self.actual += 1
						self.q = 0
			else:
				self.colaActual = 2
			
		elif self.colaActual == 2:
			estados = [p1.estado for p1 in self.procesos]
			priors = [p2.prioridad for p2 in self.procesos]
			i = self.actual % len(self.procesos)
			if 2 in priors:
				while self.procesos[i].terminado() or self.procesos[i].prioridad != 2:
					self.actual += 1
					i+=1
				if self.procesos[i].listo() and not "ejecutando" in estados:
					self.procesos[i].iniciar(momento)
				if self.procesos[i].ejecutando():
					if self.q < self.quantum2:
						self.procesos[i].ejecutar()
						self.q += 1
						if self.procesos[i].rafaga < 0:
							self.procesos[i].finalizar(momento)
							self.actual += 1
							self.q = 0
							proceso = i
					else:
						self.procesos[i].alistar()
						self.procesos[i].degradar()
						self.actual += 1
						self.q = 0
			else:
				self.colaActual = 3
		elif self.colaActual == 3:
			estados = [p.estado for p in self.procesos]
			if 3 in priors:
				for p in self.procesos:
					if not p.terminado():
						menor = min(menor, p.rafaga)
				for p in self.procesos:
					if "ejecutando" not in estados and "listo" in estados:
						if menor == p.rafaga and p.listo():
							p.iniciar(momento)
							break
				for p in self.procesos:
					if p.ejecutando():
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

