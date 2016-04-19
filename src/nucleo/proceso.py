'''
Created on 5/04/2016
@author: Juan Pablo Moreno - 20111020059
'''
from random import randint

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
		self.estado = "bloqueado"
	
	def ejecutar(self):
		self.rafaga -= 1
		