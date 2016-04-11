'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from time import clock
from random import random
from . import Proceso

class FCFS(object):

	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
						"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		self.procesos = []
		self.cantProcesos = 0	

	def agregarProceso(self):
		if self.cantProcesos < 5 or random() < 0.4:
			proceso = Proceso(self._PROCESOS[self.cantProcesos % len(self._PROCESOS)])
			proceso.llegada = round(clock())
			self.procesos.append(proceso)
			self.cantProcesos += 1
	
	def procesoActual(self):
		return self.procesos[0]
	
	def atenderProceso(self):
		if self.procesos:
			self.procesos[0].iniciar()
		
	def terminarProceso(self):
		if self.procesos:
			if self.procesos[0].rafaga<0:
				self.procesos[0].join()
				return self.procesos.pop(0)
			
	def enProceso(self):
		return self.procesos[0].activo() if self.procesos else False

class SJF(FCFS):
	
	def __init__(self):
		super(SJF, self).__init__()
				