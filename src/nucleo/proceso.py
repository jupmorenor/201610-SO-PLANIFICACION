'''
Created on 5/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from multiprocessing import Process
from random import randrange

class Proceso(object):

	def __init__(self, nombre):
		self._proceso = Process(name=nombre, target=self._tarea)
		self.rafaga = randrange(2, 15)*100
		self.llegada = 0
	
	def _tarea(self):
		self.rafaga -= 1
		
	def iniciar(self):
		self._proceso.start()
		
	def detener(self):
		self._proceso.terminate()
	
	def join(self):
		self._proceso.join()
		
	def __repr__(self):
		return self._proceso.__repr__()
	
	def activo(self):
		self._proceso.is_alive()
		