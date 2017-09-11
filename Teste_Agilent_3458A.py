#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Created on 12/2014
Versão 1.0
@author: Lucas Igor Balthazar
"""
#Importa bibliotecas
import math
import threading
import serial
import Agilent_3458A
import time
import sys

from PyQt4 import QtCore, QtGui

from interface1 import *

class MainWindows(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # Inicializa a interface
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Volt = Agilent_3458A.GPIB()
        # menu Address
        self.ui.Addr20.triggered.connect(self.Addr20)
        self.ui.Addr21.triggered.connect(self.Addr21)
        self.ui.Addr22.triggered.connect(self.Addr22)
        self.ui.Addr23.triggered.connect(self.Addr23)
        self.ui.Addr24.triggered.connect(self.Addr24)
        self.ui.Addr25.triggered.connect(self.Addr25)
        # menu Abertura
        self.ui.action500_ns_Default_2.triggered.connect(self.Aper1)
        self.ui.action166_ms_2.triggered.connect(self.Aper2)
        self.ui.action200_ms.triggered.connect(self.Aper3)
        # menu Timer
        self.ui.action1_segundo.triggered.connect(self.Time1)
        self.ui.action2_segundos.triggered.connect(self.Time2)
        self.ui.action3_segundos.triggered.connect(self.Time3)
        self.ui.action4_segundos.triggered.connect(self.Time4)
        
        self.default()

    def default(self):
        #Action Menu Bar
        self.ui.menuPort.setEnabled(False)
        self.ui.menuBaud_Rate.setEnabled(False)
        self.ui.actionDesconectar.setEnabled(False)
        self.ui.actionConfigura.setEnabled(False)
        self.ui.menuTimer.setEnabled(False)
        self.ui.actionConectar.triggered.connect(self.Conectar)
##        self.ui.actionDesconectar.triggered.connect(self.Desconectar)
        self.ui.actionConfigura.triggered.connect(self.Configura)

    def Addr20(self):
        self.var = int(self.ui.Addr20.text())
        print(self.var)

    def Addr21(self):
        self.var = int(self.ui.Addr21.text())
        print(self.var)

    def Addr22(self):
        self.var = int(self.ui.Addr22.text())
        print(self.var)

    def Addr23(self):
        self.var = int(self.ui.Addr23.text())
        print(self.var)

    def Addr24(self):
        self.var = int(self.ui.Addr24.text())
        print(self.var)

    def Addr25(self):
        self.var = int(self.ui.Addr25.text())
        print(self.var)

###################################################################################        

    def Aper1(self):
        self.aperture = 500E-9
        self.ui.menuTimer.setEnabled(True)
        print(self.aperture)

    def Aper2(self):
        self.aperture = 166E-3
        self.ui.menuTimer.setEnabled(True)
        print(self.aperture)

    def Aper3(self):
        self.aperture = 200E-3
        self.ui.menuTimer.setEnabled(True)
        print(self.aperture)

###################################################################################

    def Time1(self):
        self.timer = 1
        self.ui.actionConfigura.setEnabled(True)
        print(self.timer)

    def Time2(self):
        self.timer = 2
        self.ui.actionConfigura.setEnabled(True)
        print(self.timer)

    def Time3(self):
        self.timer = 3
        self.ui.actionConfigura.setEnabled(True)
        print(self.timer)

    def Time4(self):
        self.timer = 4
        self.ui.actionConfigura.setEnabled(True)
        print(self.timer)
    
    def Conectar(self, Comando):
        try:
            self.ui.actionDesconectar.setEnabled(True)
            return self.Volt.Conectar(self.var)
        except:
            return False

    def Configura(self):
        print(self.timer)
        print(self.aperture)
        try:
            return self.Volt.Config_Single(self.aperture, self.timer)
        except:
            return False  

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.LabelAbertura = QtGui.QLabel
        self.LabelTimer = QtGui.QLabel('Timer:')


###################################################################################        
class interface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        # Inicia Interface Gráfica
        self.App = QtGui.QApplication(sys.argv)
        self.myapp = MainWindows()
        self.myapp.show()
        self.App.exec_()


##class interface(object):
##    def __init__(self):
##        # Inicia Interface Grafica
##        self.App = QtGui.QApplication(sys.argv)
##        self.myapp = MainWindow()
##        self.myapp.show()
##        self.App.exec_()


a = interface()
