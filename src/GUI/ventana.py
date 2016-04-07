'''
Created on 2/04/2016
@author: Juan pablo Moreno Rico - 20111020059
'''
from PyQt4.QtGui import QWidget, QFrame, QSplitter, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt4.QtGui import QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt4.QtCore import Qt, QString, QStringList
from nucleo import Admin

class Ventana(QWidget):

	def __init__(self):
		super(Ventana, self).__init__()
		
		self.iniciar = QPushButton("iniciar")
		
		self.tablaGantt = QTableWidget(5, 0)
		self.tablaDatos = QTableWidget(0, 7)
		self.contenedor = Admin()
		
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
		fila5 = QHBoxLayout()
		
		fila3.addWidget(tituloI)
		fila4.addWidget(self.tablaDatos)
		fila5.addWidget(self.iniciar)
		
		cajaInferior = QVBoxLayout()
		
		cajaInferior.addLayout(fila3)
		cajaInferior.addLayout(fila4)
		cajaInferior.addLayout(fila5)
		
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
		self._configurar()
		self.show()
		
	def _configurar(self):
		self.iniciar.clicked.connect(self._comenzar)
		
		self.tablaGantt.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaGantt.setDragDropOverwriteMode(False)
		nProcesos = [proceso.nombre() for proceso in self.contenedor.procesos]
		self.tablaGantt.setVerticalHeaderLabels(QStringList(nProcesos))
		
		self.tablaDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaDatos.setDragDropOverwriteMode(False)
		datos = ["PROCESO", "LLEGADA", "RAFAGA", "COMIENZO", "FINALIZACION", "RETORNO", "ESPERA"]
		self.tablaDatos.setHorizontalHeaderLabels(QStringList(datos))
		
		self.tablaDatos.setRowCount(5)
	
		for j in range(self.contenedor.cantProcesos):
			self.tablaDatos.setItem(j, 0, QTableWidgetItem(self.contenedor.procesos[j].nombre()))
			self.tablaDatos.setItem(j, 1, QTableWidgetItem(str(self.contenedor.procesos[j].llegada)))
			self.tablaDatos.setItem(j, 2, QTableWidgetItem(str(self.contenedor.procesos[j].rafaga/100)))
		
		self.tablaGantt.setColumnCount(5)
		for i in range(5):	
			for j in range(self.contenedor.cantProcesos):
				if i>=j:
					item = QTableWidgetItem()
					item.setBackgroundColor(Qt.red)
					self.tablaGantt.setItem(j, i, item)
		
		self.tablaGantt.resizeColumnsToContents()
		self.tablaDatos.resizeColumnsToContents()	
	
	def _comenzar(self):
		while self.contenedor.cantProcesos < 10:
			while self.contenedor.enProceso():
				self.contenedor.terminarProceso()
		
		msj = QMessageBox.information(self, "Terminado", "El proceso de simulacion ha terminado")
		
		
		