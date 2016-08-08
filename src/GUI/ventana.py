'''
Created on 2/04/2016
@author: Juan pablo Moreno Rico - 20111020059
'''
from time import clock
from PyQt4.QtGui import QWidget, QFrame, QSplitter, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QColor
from PyQt4.QtGui import QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QInputDialog
from PyQt4.QtCore import Qt, QStringList, QTimer
from nucleo import FCFS, SJF, SRTF, Prioridad, RoundRobin, MulticolasRetro

class Ventana(QWidget):

	def __init__(self):
		super(Ventana, self).__init__()
		self.algoritmos = {"FCFS":FCFS, "SJF":SJF, "SRTF":SRTF, "Prioridad":Prioridad, "Round Robin":RoundRobin, "Colas multiples retroalimentadas":MulticolasRetro}
		self.iniciar = QPushButton("INICIAR")
		self.bloquear = QPushButton("BLOQUEAR")
		self.tablaGantt = QTableWidget(5, 0)
		self.tablaDatos = QTableWidget(0, 9)
		self.temporizador = QTimer(self)
		self.contenedor = None
		self.cant = 0
		self.terminados = 0
		self.fila = 0
		self.columna = 0
		self.bloqueo = False
		
		self._inicializar()
	
	def _inicializar(self):
		self.setWindowTitle("Algoritmos de planificacion ")
		
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
		fila5.addWidget(self.bloquear)
		
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
		
		self.setFixedSize(1200, 900)
		self._configurar()
		self.show()
		
	def _configurar(self):
		self.iniciar.clicked.connect(self._comenzar)
		self.bloquear.clicked.connect(self._bloquear)
		self.bloquear.setEnabled(False)
		self.temporizador.timeout.connect(self._actualizar)
		self.tablaGantt.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaGantt.setDragDropOverwriteMode(False)
		
		self.tablaDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tablaDatos.setDragDropOverwriteMode(False)
		datos = ["PROCESO", "LLEGADA", "RAFAGA", "PRIORIDAD", "EDAD", "COMIENZO", "FINALIZACION", "RETORNO", "ESPERA"]
		self.tablaDatos.setHorizontalHeaderLabels(QStringList(datos))

	def _comenzar(self):
		ok = 0
		eleccion, ok1 = QInputDialog.getItem(self, "Algoritmos", "Seleccione un algoritmo", self.algoritmos.keys())
		if ok1:
			self.contenedor = self.algoritmos[str(eleccion)]()
			self.cant, ok = QInputDialog.getInt(self, "Duracion", "Indique la duracion de la simulacion", min=0, max=60)
		if ok and ok1:
			self.setWindowTitle(self.windowTitle() + " --" +str(eleccion))
			self.temporizador.start(1000)
			self.iniciar.setEnabled(False)
			self.bloquear.setEnabled(True)
		self._inicializarDatos()
			
	def _bloquear(self):
		self.bloqueo = True
	
	def _actualizar(self):
		momento = round(clock())
		if momento < self.cant:
			proceso = self.contenedor.agregarProcesos(momento)
			if proceso:
				if proceso.listo():
					self._actualizarDatosNuevo(proceso)
					self.tablaGantt.insertRow(self.fila)
					self.fila += 1
		estados = [p.estado for p in self.contenedor.procesos]
		if self.contenedor.procesos and ("listo" in estados or "ejecutando" in estados):
			proceso = self.contenedor.administrarProcesos(momento, self.bloqueo)
			if self.bloqueo:
				self.bloqueo = False
			if proceso or proceso==0:
				if self.contenedor[proceso].terminado() and not self.contenedor[proceso].actualizado:
					self._actualizarDatosFinalizado(self.contenedor[proceso], proceso)
					self.contenedor[proceso].actualizado = True
					self.terminados += 1
			self._actualizarGantt()
			if isinstance(self.contenedor, Prioridad):
				self._actualizarDatosDinamicos()
			
		else:
			msj = QMessageBox.information(self, "Terminado", "El proceso de simulacion ha terminado")
			self.temporizador.stop()	
			del msj 
		
	def _actualizarGantt(self):
		self.tablaGantt.insertColumn(self.columna)
		for i in range(len(self.contenedor)):
			item = QTableWidgetItem()
			if self.contenedor[i].ejecutando():
				if self.contenedor[i].prioridad == 1:
					item.setBackgroundColor(QColor(0,128,0))
				elif self.contenedor[i].prioridad == 2:
					item.setBackgroundColor(QColor(0,255,0))
				elif self.contenedor[i].prioridad == 3:
					item.setBackgroundColor(QColor(128,255,128))
			elif self.contenedor[i].listo():
				if self.contenedor[i].prioridad == 1:
					item.setBackgroundColor(QColor(128,0,0))
				elif self.contenedor[i].prioridad == 2:
					item.setBackgroundColor(QColor(255,0,0))
				elif self.contenedor[i].prioridad == 3:
					item.setBackgroundColor(QColor(255,128,128))
			elif self.contenedor[i].bloqueado():
				item.setBackgroundColor(Qt.blue)
			self.tablaGantt.setItem(i, self.columna, item)
		self.columna += 1
		self.tablaGantt.resizeColumnsToContents()

	def _actualizarDatosNuevo(self, proceso):
		self.tablaDatos.insertRow(self.fila)
		self.tablaDatos.setItem(self.fila, 0, QTableWidgetItem(str(proceso.nombre)))
		self.tablaDatos.setItem(self.fila, 1, QTableWidgetItem(str(proceso.llegada)))
		self.tablaDatos.setItem(self.fila, 2, QTableWidgetItem(str(proceso.rafaga)))
		if isinstance(self.contenedor, Prioridad):
			self.tablaDatos.setItem(self.fila, 3, QTableWidgetItem(str(proceso.prioridad)))
			self.tablaDatos.setItem(self.fila, 4, QTableWidgetItem(str(proceso.edad)))
		self.tablaDatos.resizeColumnsToContents()

	def _actualizarDatosDinamicos(self):
		for i in range(len(self.contenedor)):
			self.tablaDatos.setItem(i, 3, QTableWidgetItem(str(self.contenedor[i].prioridad)))
			self.tablaDatos.setItem(i, 4, QTableWidgetItem(str(self.contenedor[i].edad)))

	def _actualizarDatosFinalizado(self, proceso, i):
		self.tablaDatos.setItem(i, 5, QTableWidgetItem(str(proceso.comienzo)))
		self.tablaDatos.setItem(i, 6, QTableWidgetItem(str(proceso.finalizacion)))
		self.tablaDatos.setItem(i, 7, QTableWidgetItem(str(proceso.finalizacion - proceso.llegada)))
		self.tablaDatos.setItem(i, 8, QTableWidgetItem(str(proceso.comienzo - proceso.llegada)))
	
	def _inicializarDatos(self):
		for i in range(len(self.contenedor)):
			self.tablaDatos.insertRow(self.fila)
			self.tablaDatos.setItem(self.fila, 0, QTableWidgetItem(str(self.contenedor[i].nombre)))
			self.tablaDatos.setItem(self.fila, 1, QTableWidgetItem(str(self.contenedor[i].llegada)))
			self.tablaDatos.setItem(self.fila, 2, QTableWidgetItem(str(self.contenedor[i].rafaga)))
			if isinstance(self.contenedor, Prioridad):
				self.tablaDatos.setItem(self.fila, 3, QTableWidgetItem(str(self.contenedor[i].prioridad)))
				self.tablaDatos.setItem(self.fila, 4, QTableWidgetItem(str(self.contenedor[i].edad)))
			self.fila += 1
		self.tablaDatos.resizeColumnsToContents()
	