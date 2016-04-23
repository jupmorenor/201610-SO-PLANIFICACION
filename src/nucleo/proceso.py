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
		self.actualizado = False
		self.prioridad = randint(1,4)
		self.edad = randint(4, 8)
		
	def iniciar(self, com):
		self.estado = "ejecutando"
		self.comienzo = com
		
	def finalizar(self, fin):
		self.estado = "terminado"
		self.finalizacion = fin
	
	def bloquear(self):
		self.estado = "bloqueado"
	
	def ejecutar(self):
		self.rafaga -= 1
		
	def envejecer(self):
		self.edad -= 1
		
	def priorizar(self):
		self.prioridad -= 1
		if self.prioridad > 1:
			self.edad = randint(10, 15)
		