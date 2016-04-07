'''
Created on 6/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from time import clock, sleep
from random import random
from . import Proceso

class Admin(object):

	def __init__(self):
		self._PROCESOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
		self.procesos = []
		self.proceso_actual = None
		self.cantProcesos = 0
		self._inicializar()
	
	def _inicializar(self):
		#random.seed()
		for i in range(5):
			proceso = Proceso(self._PROCESOS[self.cantProcesos])
			proceso.llegada = round(clock())
			self.procesos.append(proceso)
			self.cantProcesos += 1
			sleep(1)
			
	def agregarProceso(self):
		if random()*100 > 50:
			proceso = Proceso(self._PROCESOS[self.cantProcesos])
			proceso.llegada = round(clock())
			self.procesos.append(proceso)
			self.cantProcesos += 1
	
	def atenderProceso(self):
		self.proceso_actual = self.procesos.pop(0)
		self.proceso_actual.iniciar()
		
	def terminarProceso(self):
		if self.proceso_actual.rafaga<0:
			self.proceso_actual.join()
			
	def enProceso(self):
		return self.proceso_actual.activo()
		