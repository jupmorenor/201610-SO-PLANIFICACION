'''
Created on 5/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from multiprocessing import Process

class Proceso(object):

	def __init__(self, nombre):
		self.proceso = Process(name=nombre, target=self.tarea)
	
	def tarea(self):
		pass
		
		