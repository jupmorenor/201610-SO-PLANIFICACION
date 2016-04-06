'''
Created on 2/04/2016
@author: Juan pablo Moreno Rico - 20111020059
'''
import sys
from PyQt4.QtGui import QApplication
from GUI import Ventana

def main():
	app = QApplication(sys.argv)
	v = Ventana()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
