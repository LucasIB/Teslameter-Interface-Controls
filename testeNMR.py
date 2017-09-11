#coding: utf-8 -*-
import serial
import numpy as np
import time
import matplotlib.pyplot as plt

# Configuracao serial NMR
serNMR = serial.Serial(5)
serNMR.baudrate = 19200
serNMR.bytesize = serial.EIGHTBITS
serNMR.stopbits = serial.STOPBITS_ONE
serNMR.parity = serial.PARITY_NONE
serNMR.timeout = .015
if not serNMR.isOpen():
    serNMR.open()

# Comandos NMR
LerCampo = '\x05'       # Faz a leitura do valor no display. Formato: vdd.ddddddF/T
Status = 'S1'           # Descreve o stauts do equipamento  
Manual = 'A0'           # "0" = Modo Manual
Auto = 'A1'             # "1" = Modo Automatico
Remoto = 'R'            # Acesso remoto (Desabilita o painel frontal)
Local = 'L'             
Canal = 'PD'            # O Canal do multiplexador selecionado D
Coarse = 'C1400\r\n'    # 
Display = 'D1'          # Seleciona o Display

#Definições NMR

def EscreverNMR(Comando):
    serNMR.write(Comando.encode('utf-8'))

def LerNMR(Comando):
    serNMR.write(Comando.encode('utf-8'))
    return serNMR.read(20).decode('utf-8')

def LerCampoNMR():
    a = LerNMR(LerCampo)
    a = a[0:-3]
    return a

def ConfiguraNMR():
    EscreverNMR(Remoto)
    time.sleep(0.01)
    EscreverNMR(Canal)
    time.sleep(0.01)
    EscreverNMR(Coarse)
    time.sleep(0.01)
    EscreverNMR(Auto)
    time.sleep(0.01)
    EscreverNMR(Display)
    time.sleep(0.01)
    a=LerNMR(Status)
