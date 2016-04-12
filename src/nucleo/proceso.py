'''
Created on 5/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from time import sleep
from multiprocessing import Process
from random import randrange, randint

class Proceso(object):
	
	def __init__(self, nom, ll):
		self.nombre = nom
		self.rafaga = randint(2, 10)
		self.llegada = ll
		self.comienzo = 0
		self.finalizacion = 0
		self.estado = "listo"
		
	def iniciar(self, com):
		self.estado = "ejecutando"
		self.comienzo = com
		
	def finalizar(self, fin):
		self.estado = "terminado"
		self.finalizacion = fin
	
	def pausar(self):
		self.estado = "pausado"
	
	def ejecutar(self):
		self.rafaga -= 1

class Proceso2(object):

	def __init__(self, nombre):
		self._proceso = nombre#Process(name=nombre, target=self._tarea)
		self.rafaga = randrange(2, 10)
		self.llegada = 0
		self.comienzo = 0
		self.finalizacion = 0
		self.pausado = False
	
	def _tarea(self):
		if not self.pausado:
			self.rafaga -= 1
		
	def iniciar(self):
		self._proceso.start()
		
	def detener(self):
		self._proceso.terminate()
	
	def join(self):
		self._proceso.join()
		
	def nombre(self):
		return self._proceso.name
	
	def activo(self):
		self._proceso.is_alive()
		