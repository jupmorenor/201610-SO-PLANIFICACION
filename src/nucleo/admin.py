'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from random import random
from . import Proceso, ProcesoPriorizable

class _Administrador(object):
	
	def __init__(self, prior=False):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self._prior = prior
		self._inicializar()
	
	def _inicializar(self):
		for i in range(5):
			if self._prior:
				proceso = ProcesoPriorizable(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], 0.0)
			else:
				proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], 0.0)
			self.procesos.append(proceso)
	
	def agregarProcesos(self, momento):
		if random() < 0.2:
			if self._prior:
				proceso = ProcesoPriorizable(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], 0.0)
			else:
				proceso = Proceso(self._PROCESOS[len(self.procesos) % len(self._PROCESOS)], momento)
			self.procesos.append(proceso)
			return proceso
		return None
	
	def administrarProcesos(self, momento, bloqueo):
		pass
	
	def __len__(self):
		return len(self.procesos)
	
	def __getitem__(self, i):
		return self.procesos[i]
	

class FCFS(_Administrador):
	
	def __init__(self):
		super(FCFS, self).__init__()
		self.actual = 0
	
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
				break
		i = self.actual % len(self.procesos)
		while self.procesos[i].terminado():
			self.actual += 1
			i+=1
		if self.procesos[i].listo():
			self.procesos[i].iniciar(momento)
		if self.procesos[i].ejecutando():
			self.procesos[i].ejecutar()
			if self.procesos[i].rafaga < 0:
				self.procesos[i].finalizar(momento)
				proceso = i
				self.actual += 1
		return proceso
	

class SJF(_Administrador):
	
	def __init__(self):
		super(SJF, self).__init__()
	
	def administrarProcesos(self, momento, bloqueo):
		for p in self.procesos:
			if p.bloqueado():
				p.alistar()
				break
		for p in self.procesos:
			if bloqueo and p.ejecutando():
				p.bloquear()
				break
		proceso = None
		menor = 20
		estados = [p.estado for p in self.procesos]
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
		return proceso
	

class SRTF(SJF):
	
	def __init__(self):
		super(SRTF, self).__init__()
	

class Prioridad(_Administrador):
	
	def __init__(self):
		super(Prioridad, self).__init__(prior=True)
		
	def administrarProcesos(self, momento, bloqueo):
		proceso = None
		menor = 20
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
			if menor < p.prioridad and p.ejecutando():
				p.alistar()
			estados = [p1.estado for p1 in self.procesos]
			if menor == p.prioridad and p.listo() and not "ejecutando" in estados:
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
	

class RoundRobin(FCFS):
	
	def __init__(self):
		super(RoundRobin, self).__init__()
		self.quantum = 5
		self.q = 0

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
		while self.procesos[i].terminado():
			self.actual += 1
			i+=1
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
	
