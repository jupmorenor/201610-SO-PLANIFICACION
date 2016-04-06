'''
Created on 2/04/2016
@author: Juan pablo Moreno Rico - 20111020059
'''
from PyQt4.QtGui import QWidget, QFrame, QSplitter, QHBoxLayout, QVBoxLayout, QLabel
from PyQt4.QtGui import QPushButton, QTableWidget, QTableWidgetItem
from PyQt4.QtCore import Qt

class Ventana(QWidget):

	def __init__(self):
		super(Ventana, self).__init__()
		
		self.iniciar = QPushButton("iniciar")
		
		self.tablaGantt = QTableWidget(15,15)
		self.tablaDatos = QTableWidget(15,15)
		
		self._inicializar()
	
	def _inicializar(self):
		self.setWindowTitle("FCFS")
		
		#------------------------------------#
		#	ELEMENTOS DEL PANEL SUPERIOR 	 #
		#------------------------------------#
		
		tituloS = QLabel("DIAGRAMA DE GANTT")
		
		tituloS.adjustSize()
		
		fila1 = QHBoxLayout()
		fila2 = QHBoxLayout()
		
		fila1.addWidget(tituloS)
		fila2.addWidget(self.tablaGantt)
		
		cajaSuperior = QVBoxLayout()
		
		cajaSuperior.addLayout(fila1)
		cajaSuperior.addLayout(fila2)
		
		#------------------------------------#
		#	ELEMENTOS DEL PANEL INFERIOR 	 #
		#------------------------------------#
		
		tituloI = QLabel("DATOS DE LOS PROCESOS")
		
		tituloI.adjustSize()
		
		fila3 = QHBoxLayout()
		fila4 = QHBoxLayout()
		
		fila3.addWidget(tituloI)
		fila4.addWidget(self.tablaDatos)
		
		cajaInferior = QVBoxLayout()
		
		cajaInferior.addLayout(fila3)
		cajaInferior.addLayout(fila4)
		
		#------------------------------------#
						
		#agregar el segundo nivel de layout al panel
		panelSuperior = QFrame(self)
		panelSuperior.setFrameShape(QFrame.StyledPanel)
		panelSuperior.setLayout(cajaSuperior)
		
		#agregar el segundo nivel de layout al panel
		panelInferior = QFrame(self)
		panelInferior.setFrameShape(QFrame.StyledPanel)
		panelInferior.setLayout(cajaInferior)
		
		#agregar el panel al separador
		separador = QSplitter(Qt.Vertical)
		separador.addWidget(panelSuperior)
		separador.addWidget(panelInferior)
		
		#agregar el separador al primer layout
		caja = QVBoxLayout(self)
		caja.addWidget(separador)
		
		#agregar el layout a la ventana
		self.setLayout(caja)
		
		self.setFixedSize(800, 600)
		self.show()
		
		
		