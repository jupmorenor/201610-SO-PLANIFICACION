'''
Created on 5/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from time import sleep
from multiprocessing import Process
from random import randrange

class Proceso(object):

	def __init__(self, nombre):
		self._proceso = Process(name=nombre, target=self._tarea)
		self.rafaga = randrange(2, 10)
		self.llegada = 0
		self.comienzo = 0
		self.finalizacion = 0
		self.pausado = False
	
	def _tarea(self):
		if not self.pausado:
			sleep(self.rafaga)
		
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
		