'''
Created on 2/04/2016
@author: Juan pablo Moreno Rico - 20111020059
'''
from time import clock
from PyQt4.QtGui import QWidget, QFrame, QSplitter, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt4.QtGui import QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QInputDialog
from PyQt4.QtCore import Qt, QStringList, QTimer
from nucleo import FCFS, SJF, SRTF, Proceso

class Ventana(QWidget):

	def __init__(self):
		super(Ventana, self).__init__()
		self.algoritmos = {"FCFS":FCFS, "SJF":SJF, "SRTF":SRTF, "Round Robin":None}
		self.iniciar = QPushButton("INICIAR")
		self.bloquear = QPushButton("BLOQUEAR")
		self.tablaGantt = QTableWidget()
		self.tablaDatos = QTableWidget(0, 7)
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
		
		self.setFixedSize(800, 600)
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
		datos = ["PROCESO", "LLEGADA", "RAFAGA", "COMIENZO", "FINALIZACION", "RETORNO", "ESPERA"]
		self.tablaDatos.setHorizontalHeaderLabels(QStringList(datos))

	def _comenzar(self):
		ok = 0
		eleccion, ok1 = QInputDialog.getItem(self, "Algoritmos", "Seleccione un algoritmo", self.algoritmos.keys())
		if ok1:
			self.contenedor = self.algoritmos[str(eleccion)]()
			self.cant, ok = QInputDialog.getInt(self, "Cantidad", "Indique la cantidad de procesos", min=0, max=50)
		if ok and ok1:
			self.setWindowTitle(self.windowTitle() + " --" +str(eleccion))
			self.temporizador.start(1000)
			self.iniciar.setEnabled(False)
			self.bloquear.setEnabled(True)
			
	def _bloquear(self):
		self.bloqueo = True
	
	def _actualizar(self):
		momento = round(clock())
		if self.contenedor.cantProcesos < self.cant:
			proceso = self.contenedor.agregarProcesos(momento)
			if proceso is not None:
				if proceso.estado == "listo":
					self._actualizarDatosNuevo(proceso)
					self.tablaGantt.insertRow(self.fila)
					self.fila += 1
		if self.contenedor.procesos:
			proceso = self.contenedor.administrarProcesos(momento)
			if self.bloqueo:
				self.bloqueo = False
			if isinstance(proceso, Proceso):
				if proceso.estado == "terminado":
					self._actualizarDatosFinalizado(proceso)
					self.terminados += 1
			elif isinstance(proceso, int):
				if self.contenedor.procesos[proceso].estado == "terminado" and not self.contenedor.procesos[proceso].actualizado:
					self._actualizarDatosFinalizado(self.contenedor.procesos[proceso])
					self.contenedor.procesos[proceso].actualizado = True
					self.terminados += 1
			self._actualizarGantt()
			
		else:
			msj = QMessageBox.information(self, "Terminado", "El proceso de simulacion ha terminado")
			self.temporizador.stop()	
			del msj
		
	def _actualizarGantt(self):
		self.tablaGantt.insertColumn(self.columna)
		if isinstance(self.contenedor, FCFS):
			for i in range(self.terminados, self.fila):
				item = QTableWidgetItem()
				if self.contenedor.procesos[i - self.terminados].estado == "ejecutando":
					item.setBackgroundColor(Qt.green)
				elif self.contenedor.procesos[i - self.terminados].estado == "listo":
					item.setBackgroundColor(Qt.red)
				elif self.contenedor.procesos[i - self.terminados].estado == "bloqueado":
					item.setBackgroundColor(Qt.blue)
				self.tablaGantt.setItem(i, self.columna, item)		
		elif isinstance(self.contenedor, SJF):
			for i in range(self.contenedor.cantProcesos):
				item = QTableWidgetItem()
				if self.contenedor.procesos[i].estado == "ejecutando":
					item.setBackgroundColor(Qt.green)
				elif self.contenedor.procesos[i].estado == "listo":
					item.setBackgroundColor(Qt.red)
				elif self.contenedor.procesos[i].estado == "bloqueado":
					item.setBackgroundColor(Qt.blue)
				self.tablaGantt.setItem(i, self.columna, item)
				
		self.columna += 1
		self.tablaGantt.resizeColumnsToContents()
		
	def _actualizarDatosNuevo(self, proceso):
		self.tablaDatos.insertRow(self.fila)
		self.tablaDatos.setItem(self.fila, 0, QTableWidgetItem(str(proceso.nombre)))
		self.tablaDatos.setItem(self.fila, 1, QTableWidgetItem(str(proceso.llegada)))
		self.tablaDatos.setItem(self.fila, 2, QTableWidgetItem(str(proceso.rafaga)))
		self.tablaDatos.resizeColumnsToContents()

	def _actualizarDatosFinalizado(self, proceso):
		self.tablaDatos.setItem(self.terminados, 3, QTableWidgetItem(str(proceso.comienzo)))
		self.tablaDatos.setItem(self.terminados, 4, QTableWidgetItem(str(proceso.finalizacion)))
		self.tablaDatos.setItem(self.terminados, 5, QTableWidgetItem(str(proceso.finalizacion - proceso.llegada)))
		self.tablaDatos.setItem(self.terminados, 6, QTableWidgetItem(str(proceso.comienzo - proceso.llegada)))
		
		
		