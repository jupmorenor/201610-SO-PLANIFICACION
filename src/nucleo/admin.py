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
		
	def administrarProcesos(self, momento):
		if self.cantProcesos < 2 or random() < 0.25:
			proceso = Proceso(self._PROCESOS[self.cantProcesos % len(self._PROCESOS)], momento)
			self.procesos.append(proceso)
			self.cantProcesos += 1
			return proceso
		if self.procesos:
			if self.procesos[0].estado == "listo":
				self.procesos[0].iniciar(momento)
			elif self.procesos[0].estado == "ejecutando":
				self.procesos[0].ejecutar()
				if self.procesos[0].rafaga <= 0:
					self.procesos[0].finalizar(momento)
			elif self.procesos[0].estado == "terminado":
				return self.procesos.pop(0)
		return None

class FCFS2(object):

	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self.cantProcesos = 0	

	def agregarProceso(self, momento):
		if self.cantProcesos < 5 or random() < 0.25:
			proceso = Proceso(self._PROCESOS[self.cantProcesos % len(self._PROCESOS)])
			proceso.llegada = round(momento)
			self.procesos.append(proceso)
			self.cantProcesos += 1
			return True
		return False
	
	def procesoActual(self):
		return self.procesos[0]
	
	def nuevoProceso(self):
		if self.procesos:
			return self.procesos[len(self.procesos)-1] 
	
	def atenderProceso(self, momento):
		if self.procesos:
			if not self.enProceso():
				self.procesos[0].iniciar()
				self.procesos[0].comienzo = momento
				#return True
		#return False
		
	def terminarProceso(self, momento):
		if self.procesos:
			if not self.enProceso():
				self.procesos[0].join()
				self.procesos[0].finalizacion = momento
				return self.procesos.pop(0)
		return None
			
	def enProceso(self):
		return self.procesos[0].activo() if self.procesos else False

class SJF(FCFS):
	
	def __init__(self):
		super(SJF, self).__init__()
				