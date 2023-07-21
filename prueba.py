#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import sqlite3

from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,
                         QRegExpValidator)
from PyQt5.QtCore import (Qt, QFile, QDate, QTime, QSize, QTimer, QRect, QRegExp, QTranslator,
                          QLocale, QLibraryInfo)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDialog, QTableWidget, QMenu,
                             QTableWidgetItem, QAbstractItemView, QLineEdit, QPushButton,
                             QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox,
                             QDateEdit, QComboBox)


from patsy import dmatrices
from PyQt5 import uic, QtWidgets
import sys
from PyQt5.QtCore import pyqtSlot 
from PyQt5.QtWidgets import QDialog, QMainWindow,QPushButton, QFrame, QApplication, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import sqlite3
import base64
import time
import datetime
import re
from sqlite3 import Error


qtCreatorFile = "simple.ui" #Aquí va el nombre de tu archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        
        #Aquí van los botones
        self.boton1.clicked.connect(self.simple_collect)
        self.boton2.clicked.connect(self.upload_data)
        self.boton3.clicked.connect(self.limpiar)
        self.boton4.clicked.connect(self.eliminarFila)
        self.boton4.clicked.connect(self.eliminarFila)
        self.boton5.clicked.connect(self.Eliminar)
        
        
        


    def simple_collect(self):
        conn = sqlite3.connect('simple_database.db')
        c = conn.cursor()
        nombre = str(self.lineEdit.text())
        nombre = nombre.upper()## para poner todo en mayusculas
        edad = str(self.lineEdit_2.text())
        edad = edad.upper()
        sexo = str(self.lineEdit_3.text())
        sexo = sexo.upper()
        peso = str(self.lineEdit_4.text())
        estatura = str(self.lineEdit_5.text())
        pais = str(self.lineEdit_6.text())
        pais = pais.upper() 
    

        c.execute('INSERT INTO simple_info(nombre, edad, sexo, peso, estatura, pais) VALUES (?, ?, ?, ?, ?,?)',
        	   (nombre,edad,sexo,peso,estatura,pais))

        conn.commit()
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')



    def upload_data(self):

    	conn = sqlite3.connect('simple_database.db')
    	c = conn.cursor()

    	query = 'SELECT * FROM simple_info'
    	result = c.execute(query)

    	self.tableWidget.setRowCount(0)
    	for row_number, row_data in enumerate(result):
    		self.tableWidget.insertRow(row_number)
    		for column_number, data in enumerate(row_data):
    			self.tableWidget.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))

    def limpiar(self):
         
         self.tableWidget.clearContents()
         self.tableWidget.setRowCount(0)
           

    def eliminarFila(self):
        filaSeleccionada = self.tableWidget.selectedItems()

        if filaSeleccionada:
            fila = filaSeleccionada[0].row()
            self.tableWidget.removeRow(fila)
           
            self.tableWidget.clearSelection()
        #else:
            #QMessageBox.critical(self, "Eliminar fila", "Seleccione la fila.   ",
                               # QMessageBox.Ok)

    def Eliminar(self):
        fila = self.tableWidget.selectedItems()
        

        if fila:
            eliminar = QMessageBox(self)

            eliminar.setWindowTitle("Eliminar registro")
            eliminar.setIcon(QMessageBox.Question)
            eliminar.setText("¿Esta seguro que desea eliminar el registro?   ")
            botonSi = eliminar.addButton("Si", QMessageBox.YesRole)
            botonCancelar = eliminar.addButton("Cancelar", QMessageBox.NoRole)
                
            eliminar.exec_()
                
            if eliminar.clickedButton() == botonSi:
                indiceFila = fila[0].row()
                nombre_d = self.tableWidget.item(indiceFila, 0).text()

                if QFile.exists("simple_database.db"):
                    conexion = sqlite3.connect("simple_database.db")
                    cursor = conexion.cursor()
                        
                    try:
                        cursor.execute("DELETE FROM simple_info WHERE nombre = ?", (nombre_d,))
                        conexion.commit()

                        conexion.close()

                        self.tableWidget.removeRow(indiceFila)
                        self.tableWidget.clearSelection()

                        QMessageBox.information(self, "Eliminar registro", "Registro eliminado."
                                                "   ", QMessageBox.Ok)
                    except:
                        conexion.close()
                        QMessageBox.critical(self, "Eliminar registro", "Error desconocido.   ",
                                             QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "Buscar registro", "No se encontro la base de "
                                         "datos.   ", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Eliminar registro", "Seleccione un registro.   ",
                                 QMessageBox.Ok)





if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
