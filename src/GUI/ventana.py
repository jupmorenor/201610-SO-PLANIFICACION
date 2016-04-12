'''
Created on 2/04/2016
@author: Juan pablo Moreno Rico - 20111020059
'''
from time import clock
from PyQt4.QtGui import QWidget, QFrame, QSplitter, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt4.QtGui import QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QInputDialog
from PyQt4.QtCore import Qt, QStringList, QTimer
from nucleo import FCFS

class Ventana(QWidget):

	def __init__(self):
		super(Ventana, self).__init__()
		
		self.iniciar = QPushButton("INICIAR")
		
		self.tablaGantt = QTableWidget()
		self.tablaDatos = QTableWidget(0, 7)
		self.temporizador = QTimer(self)
		self.contenedor = FCFS()
		self.cant = 0
		self.terminados = 0
		self.fila = 0
		self.columna = 0
		
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
		self.temporizador.timeout.connect(self._actualizar)
		self.tablaGantt.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaGantt.setDragDropOverwriteMode(False)
		
		self.tablaDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaDatos.setDragDropOverwriteMode(False)
		datos = ["PROCESO", "LLEGADA", "RAFAGA", "COMIENZO", "FINALIZACION", "RETORNO", "ESPERA"]
		self.tablaDatos.setHorizontalHeaderLabels(QStringList(datos))

	def _comenzar(self):
		self.cant, ok = QInputDialog.getInt(self, "Cantidad", "Indique la cantidad de procesos", min=0, max=50)
		if ok:
			self.temporizador.start(1000)
	
	def _actualizar(self):
		momento = round(clock())
		if self.contenedor.cantProcesos < self.cant:
			if self.contenedor.agregarProceso(momento):
				self._actualizarDatosNuevo()
				self.tablaGantt.insertRow(self.fila)
				self.fila += 1
			if self.contenedor.atenderProceso(momento):
				pass
			proceso = self.contenedor.terminarProceso(momento)
			if proceso is not None:
				self._actualizarDatosFinalizado(proceso)
				self.terminados += 1
			self._actualizarGantt()
		else:
			msj = QMessageBox.information(self, "Terminado", "El proceso de simulacion ha terminado")
			self.temporizador.stop()	
		
	def _actualizarGantt(self):
		self.tablaGantt.insertColumn(self.columna)
		self.columna += 1
		for i in range(self.terminados, self.fila):
			item = QTableWidgetItem()
			if i == self.terminados:
				item.setBackgroundColor(Qt.green)
			else:
				item.setBackgroundColor(Qt.red)
			self.tablaGantt.setItem(i, self.columna, item)
		self.tablaGantt.resizeColumnsToContents()
		
	def _actualizarDatosNuevo(self):
		self.tablaDatos.insertRow(self.fila)
		self.tablaDatos.setItem(self.fila, 0, QTableWidgetItem(self.contenedor.nuevoProceso().nombre()))
		self.tablaDatos.setItem(self.fila, 1, QTableWidgetItem(str(self.contenedor.nuevoProceso().llegada)))
		self.tablaDatos.setItem(self.fila, 2, QTableWidgetItem(str(self.contenedor.nuevoProceso().rafaga)))
		self.tablaDatos.resizeColumnsToContents()

	def _actualizarDatosFinalizado(self, proceso):
		self.tablaDatos.setItem(self.terminados, 3, QTableWidgetItem(str(proceso.comienzo)))
		self.tablaDatos.setItem(self.terminados, 4, QTableWidgetItem(str(proceso.finalizacion)))
		self.tablaDatos.setItem(self.terminados, 5, QTableWidgetItem(str(proceso.finalizacion - proceso.llegada)))
		self.tablaDatos.setItem(self.terminados, 6, QTableWidgetItem(str(proceso.comienzo - proceso.llegada)))
		
		
		