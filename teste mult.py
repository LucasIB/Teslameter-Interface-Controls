#coding: utf-8 -*-
import serial
import re
import numpy as np
import csv
import time
import matplotlib.pyplot as plt
##import glob

# Configuracao serial NMR
serNMR = serial.Serial(5)
serNMR.baudrate = 19200
serNMR.bytesize = serial.EIGHTBITS
serNMR.stopbits = serial.STOPBITS_ONE
serNMR.parity = serial.PARITY_NONE
serNMR.timeout = .015
if not serNMR.isOpen():
    serNMR.open()

#Configuracao Serial Agilent 34401 - Temp Bloco
serAg1 = serial.Serial(10)
serAg1.baudrate = 9600
serAg1.bytesize = serial.EIGHTBITS
serAg1.stopbits = serial.STOPBITS_ONE
serAg1.parity = serial.PARITY_NONE
##serAg1.timeout = .362
serAg1.timeout = 0.37
#ser.writeTimeout = 0
if not serAg1.isOpen():
    serAg1.open()


# Comandos NMR
LerCampo = '\x05'
Status = 'S1'
Manual = 'A0'
Auto = 'A1'
Remoto = 'R'
Local = 'L'
Canal = 'PD'
Coarse = 'C1400\r\n'
Display = 'D1'

#Comandos Agilent 34401
Acessar = ':SYST:REM\r\n'
Limpar = '*CLS\r\n'
Resetar = '*RST\r\n'
#VConfVolt = ':CONF:VOLT:DC 10,0.0001\r\n'
VConfVolt1 = ':CONF:RES 100,0.0001 \r\n'
VConfVolt2 = ':CONF:VOLT:DC 10,0.00003\r\n'
VConfVolt3 = ':CONF:VOLT:DC 10,0.00003\r\n'
##VConfVolt1 = ':CONF:VOLT:DC AUTO\r\n'
##VConfVolt2 = ':CONF:VOLT:DC AUTO\r\n'
Trigger = ':TRIG:SOUR EXT\r\n'
#VConfOhm = ':CONF:RES AUTO\r\n'
LerAg = 'READ?\r\n'

#Variáveis
DataHora = 0
tempG3 = 0
tempSe = 0
campo = 0
corrente = 0
c = ' '

#Constantes
ArqOut ='MEUARQUIVO.csv'

#Definições Agilent 34401 - corrente
def AcessarVolt1():
    serAg1.write(Acessar.encode('utf-8'))

def LimparVolt1():
    serAg1.write(Limpar.encode('utf-8'))

def ResetarVolt1():
    serAg1.write(Resetar.encode('utf-8'))

def ConfigurarVolt1():
    serAg1.write(VConfVolt1.encode('utf-8'))
##    serAg1.write('DISP OFF\r\n'.encode('utf-8'))
##    serAg1.write('ZERO OFF\r\n'.encode('utf-8'))
##    serAg1.write(Trigger.encode('utf-8'))
    
def LerVolt1():
##    serAg1.flushInput()
##    serAg1.flushOutput()
    serAg1.write(LerAg.encode('utf-8'))
    ValorStr = serAg1.read(20).decode('utf-8')
    ValorStr = re.sub('\n','',ValorStr)
    ValorStr = re.sub('\r','',ValorStr)
    ValorStr = re.sub('C','',ValorStr)
    valor = ConvFloat(ValorStr)
    return valor
    
def CommandsVolt1():
    AcessarVolt1()
    LimparVolt1()
    ResetarVolt1()
    ConfigurarVolt1()

#Definições Agilent 34401 - Campo Senis
def AcessarVolt2():
    serAg2.write(Acessar.encode('utf-8'))

def LimparVolt2():
    serAg2.write(Limpar.encode('utf-8'))

def ResetarVolt2():
    serAg2.write(Resetar.encode('utf-8'))

def ConfigurarVolt2():
    serAg2.write(VConfVolt2.encode('utf-8'))
    serAg2.write('DISP OFF\r\n'.encode('utf-8'))
##    serAg2.write('ZERO OFF\r\n'.encode('utf-8'))
##    serAg2.write(Trigger.encode('utf-8'))
    
def LerVolt2():
    serAg2.write(LerAg.encode('utf-8'))
    ValorStr = serAg2.read(20).decode('utf-8')
    ValorStr = re.sub('\n','',ValorStr)
    ValorStr = re.sub('\r','',ValorStr)
    ValorStr = re.sub('C','',ValorStr)
    valor = ConvFloat(ValorStr)
    return valor
    
def CommandsVolt2():
    AcessarVolt2()
    LimparVolt2()
    ResetarVolt2()
    ConfigurarVolt2()

#Definições Agilent 34401 - Temperatura Senis
def AcessarVolt3():
    serAg3.write(Acessar.encode('utf-8'))

def LimparVolt3():
    serAg3.write(Limpar.encode('utf-8'))

def ResetarVolt3():
    serAg3.write(Resetar.encode('utf-8'))

def ConfigurarVolt3():
    serAg3.write(VConfVolt3.encode('utf-8'))
    serAg3.write('DISP OFF\r\n'.encode('utf-8'))
##    serAg3.write('ZERO OFF\r\n'.encode('utf-8'))
##    serAg3.write(Trigger.encode('utf-8'))
    
def LerVolt3():
    serAg3.write(LerAg.encode('utf-8'))
    ValorStr = serAg3.read(20).decode('utf-8')
    ValorStr = re.sub('\n','',ValorStr)
    ValorStr = re.sub('\r','',ValorStr)
    ValorStr = re.sub('C','',ValorStr)
    valor = ConvFloat(ValorStr)
    return valor
    
def CommandsVolt3():
    AcessarVolt3()
    LimparVolt3()
    ResetarVolt3()
    ConfigurarVolt3()

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

#Configurações Iniciais

def Config():
    CommandsVolt1()
    CommandsVolt2()
    CommandsVolt3()
    ConfiguraNMR()
    
##    CriaArquivo()

def CriaArquivo():
    c = csv.writer(open(ArqOut, "w"))
    c.writerow(["Data Hora","Temperatura","CampoG3","Corrente"])

def EscreverResultados():
    c.writerow([Datahora,temp,campoG3,corrente])


#Rotinas

def ConvFloat(valorStr):
    try:
        valor = float(valorStr)
    except:
        valor = 0
    return valor


def LerG3(tipo):
    if tipo == 0:
        EscreverG3(LerTemp)
        ValorStr = Ler()
        # Trata variavel
        ValorStr = ValorStr.decode('utf-8')
        ValorStr = re.sub('\n','',ValorStr)
        ValorStr = re.sub('\r','',ValorStr)
        ValorStr = re.sub('C','',ValorStr)
        valor = float(ValorStr)
        
    else:
        EscreverG3(LerCampo)
        ValorStr = Ler()
        # Trata variavel
        ValorStr = ValorStr.decode('utf-8')
        ValorStr = re.sub('\n','',ValorStr)
        ValorStr = re.sub('\r','',ValorStr)
        ValorStr = re.sub('G','',ValorStr)
        valor = float(ValorStr)

    return valor

def LerLoop(npontos):
    # Configura Group3
    ConfiguraG3()

    # Criar lista vazia
    listatempG3 = np.array([])
    listacampoG3 = np.array([])
    listatempSe = np.array([])
    listacampoSe = np.array([])
    listadatahora = np.array([])
#    listacorrente = np.array([])
    listatempB = np.array([])

    conta = 0
    tempB =  (LerVolt1()-100)/0.385
  
    for i in range(npontos):
        tempG3 = LerG3(0)
        campoG3 =  LerG3(1)
        tempSe =  LerVolt3()/0.05
        campoSe =  (LerVolt2()/0.0005)*(-1)
##        corrente = LerVolt1()*60
##        corrente =  LerVolt1()*(-1)
        tempB =  (LerVolt1()-100)/0.385
        Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
        Datahora = str(Datahora)
        listatempG3 = np.append(listatempG3,tempG3)
        listacampoG3 = np.append(listacampoG3,campoG3)
        listatempSe = np.append(listatempSe,tempSe)
        listacampoSe = np.append(listacampoSe,campoSe)
        listadatahora = np.append(listadatahora,Datahora)
##        listacorrente = np.append(listacorrente,corrente)
        listatempB = np.append(listatempB,tempB)
        tempG3 = '{0:.2f}'.format(tempG3)
        campoG3 = '{0:.2f}'.format(campoG3)
        tempSe = '{0:.2f}'.format(tempSe)
        campoSe = '{0:.3f}'.format(campoSe)
        tempB = '{0:.3f}'.format(tempB)
##        corrente = '{0:.3f}'.format(corrente)
##        print('{} Data-Hora = {}\t Temperatura G3[ºC] = {}\t Temperatura Senis[ºC] = {}\t Campo G3[G] = {}\t\t Campo Senis[G] = {}\t Corrente[A] = {}'.format(i+1,Datahora,tempG3,tempSe,campoG3,campoSe,corrente))
        print('{} Data-Hora = {}\t Temperatura G3[ºC] = {}\t Temperatura Senis[ºC] = {}\t Campo G3[G] = {}\t Campo Senis[G] = {}\t Temp Bloco[°C] = {}'.format(i+1,Datahora,tempG3,tempSe,campoG3,campoSe,tempB))
        
##    print('DataHora:'+DataHora)
    print (' ')
    print ('Campo G3')
    print ('Media: {}'.format(listacampoG3.mean()))
    print ('Desvio: {}'.format(listacampoG3.std()))

    print ('Min: {}'.format(listacampoG3.min()))
    print ('Max: {}'.format(listacampoG3.max()))

    print (' ')
    print ('Campo Senis')
    print ('Media: {}'.format(listacampoSe.mean()))
    print ('Desvio: {}'.format(listacampoSe.std()))
    print ('Min: {}'.format(listacampoSe.min()))
    print ('Max: {}'.format(listacampoSe.max()))

##    print (' ')
##    print ('Corrente')
##    print ('Media: {}'.format(listacorrente.mean()))
##    print ('Desvio: {}'.format(listacorrente.std()))
##    print ('Min: {}'.format(listacorrente.min()))
##    print ('Max: {}'.format(listacorrente.max()))

    SalvaArqs(listadatahora,listatempG3, listatempSe, listacampoG3, listacampoSe,listatempB)
##    SalvaArqs(listadatahora,listatempG3, listatempSe, listacampoG3, listacampoSe,listacorrente)
    GeraGraf(listacampoG3,listacampoSe)


def LerLoop2(npontos):
    # Configura Group3
    ConfiguraG3()

    # Criar lista vazia
    listatempG3 = np.array([])
    listacampoG3 = np.array([])
    listatempSe = np.array([])
    listacampoSe = np.array([])
    listadatahora = np.array([])
    listatempB = np.array([])

    conta = 0
    tempB =  (LerVolt1()-100)/0.385
  
    for i in range(npontos):
        tempG3 = 0
        campoG3 = 0
        tempSe = 0
        campoSe = 0
        tempB = 0
        for x in range(10):
            tempG3 = tempG3 + LerG3(0)
            campoG3 = campoG3 + LerG3(1)
            tempSe = tempSe + LerVolt3()/0.05
            campoSe = campoSe + (LerVolt2()/0.0005)*(-1)
    ##        corrente = LerVolt1()*60
            tempB = tempB + ((LerVolt1()-100)/0.385)
        tempG3 = tempG3/10
        campoG3 = campoG3/10
        tempSe = tempSe/10
        campoSe = campoSe/10
        tempB = tempB/10
        Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
        Datahora = str(Datahora)
        listatempG3 = np.append(listatempG3,tempG3)
        listacampoG3 = np.append(listacampoG3,campoG3)
        listatempSe = np.append(listatempSe,tempSe)
        listacampoSe = np.append(listacampoSe,campoSe)
        listadatahora = np.append(listadatahora,Datahora)
        listatempB = np.append(listatempB,tempB)
        tempG3 = '{0:.2f}'.format(tempG3)
        campoG3 = '{0:.2f}'.format(campoG3)
        tempSe = '{0:.2f}'.format(tempSe)
        campoSe = '{0:.3f}'.format(campoSe)
        tempB = '{0:.2f}'.format(tempB)
        print('{} Data-Hora = {}\t Temperatura G3[ºC] = {}\t Temperatura Senis[ºC] = {}\t Campo G3[G] = {}\t\t Campo Senis[G] = {}\t Temp Bloco[°C] = {}'.format(i+1,Datahora,tempG3,tempSe,campoG3,campoSe,tempB))
        time.sleep(56)
        if conta == 60:
            conta = 0
            SalvaArqs(listadatahora,listatempG3, listatempSe, listacampoG3, listacampoSe,listatempB)
        conta = conta + 1
        
##    print('DataHora:'+DataHora)
    print (' ')
    print ('Campo G3')
    print ('Media: {}'.format(listacampoG3.mean()))
    print ('Desvio: {}'.format(listacampoG3.std()))
    print ('Min: {}'.format(listacampoG3.min()))
    print ('Max: {}'.format(listacampoG3.max()))

    print (' ')
    print ('Campo Senis')
    print ('Media: {}'.format(listacampoSe.mean()))
    print ('Desvio: {}'.format(listacampoSe.std()))
    print ('Min: {}'.format(listacampoSe.min()))
    print ('Max: {}'.format(listacampoSe.max()))


    SalvaArqs(listadatahora,listatempG3, listatempSe, listacampoG3, listacampoSe,listatempB)
##    GeraGraf(listacampoG3,listacampoSe)


def LerLoop3(npontos):


    # Criar lista vazia
    listacampoNMR = np.array([])
    listastatusNMR = np.array([])
    listadatahora = np.array([])
    listatempB = np.array([])

    conta = 0
    tempB =  (LerVolt1()-100)/0.385
  
    for i in range(npontos):
        a = LerCampoNMR()
        status = a[0]
        campoNMR = float(a[1:])*10000
        tempB = (LerVolt1()-100)/0.385
        Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
        Datahora = str(Datahora)
        listacampoNMR = np.append(listacampoNMR,campoNMR)
        listastatusNMR = np.append(listastatusNMR,status)
        listadatahora = np.append(listadatahora,Datahora)
        listatempB = np.append(listatempB,tempB)
        campoNMR = '{0:.3f}'.format(campoNMR)
        tempB = '{0:.3f}'.format(tempB)
        print('{} Data-Hora = {}\t Campo NMR[T] = {} {}\t Temp Bloco[°C] = {}'.format(i+1,Datahora,status,campoNMR,tempB))
        time.sleep(59.6)
        if conta == 60:
            conta = 0
            SalvaArqs2(listadatahora,listastatusNMR,listacampoNMR,listatempB)
        conta = conta + 1
        
    SalvaArqs2(listadatahora,listastatusNMR,listacampoNMR,listatempB)
##    GeraGraf(listacampoG3,listacampoSe)

def GeraGraf(dados,dados2):
    plt.plot(dados)
    plt.plot(dados2)
    plt.show()

def SalvaArqs(D1,D2,D3,D4,D5,D6):
##    f = np.column_stack((D2, D3, D4, D5))
##    print (f)
##    np.savetxt('D:\ARQ\Ariane\Teste\Saida.txt',f, delimiter = '\t', newline='\r\n')
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','w')
    f.close()
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','a')
    tamanho = len(D1)
    for i in range (tamanho):
        f.write(D1[i]+'\t'+str(D2[i])+'\t'+str(D3[i])+'\t'+str(D4[i])+'\t'+str(D5[i])+'\t'+str(D6[i])+'\n')
    f.close()

def SalvaArqs2(D1,D2,D3,D4):
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','w')
    f.close()
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','a')
    tamanho = len(D1)
    for i in range (tamanho):
        f.write(D1[i]+'\t'+str(D2[i])+'\t'+str(D3[i])+'\t'+str(D4[i])+'\n')
    f.close()

def LerFaixas():
    # Configura Group3
    ConfiguraG3()

    # Criar lista vazia
    listatempG3 = np.array([])
    listacampoG3 = np.array([])
    listatempSe = np.array([])
    listacampoSe = np.array([])
    listadatahora = np.array([])
    listacorrente = np.array([])

    a = int(input("Entre com um número de faixas a serem lidas: "))
    
    for i in range(a):
        b = input("Aguardando...")
        for x in range(10):
            tempG3 = LerG3(0)
            campoG3 = LerG3(1)*(-1)
            tempSe = LerVolt3()/0.05
            campoSe = (LerVolt2()/0.0005)
            corrente = LerVolt1()*(-1)
            Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
            Datahora = str(Datahora)
            listatempG3 = np.append(listatempG3,tempG3)
            listacampoG3 = np.append(listacampoG3,campoG3)
            listatempSe = np.append(listatempSe,tempSe)
            listacampoSe = np.append(listacampoSe,campoSe)
            listadatahora = np.append(listadatahora,Datahora)
            listacorrente = np.append(listacorrente,corrente)
            tempG3 = '{0:.2f}'.format(tempG3)
            campoG3 = '{0:.2f}'.format(campoG3)
            tempSe = '{0:.2f}'.format(tempSe)
            campoSe = '{0:.3f}'.format(campoSe)
            corrente = '{0:.3f}'.format(corrente)
            print('{} Data-Hora = {}\t Temperatura G3[ºC] = {}\t Temperatura Senis[ºC] = {}\t Campo G3[G] = {}\t\t Campo Senis[G] = {}\t Corrente[A] = {}'.format(i+1,Datahora,tempG3,tempSe,campoG3,campoSe,corrente))

    print ('Concluído!')

    SalvaArqs(listadatahora,listatempG3, listatempSe, listacampoG3, listacampoSe,listacorrente)
    GeraGraf(listacampoG3,listacampoSe,listacorrente)


