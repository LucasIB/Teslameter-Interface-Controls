#coding: utf-8 -*-
import serial
import re
import numpy as np
import time
import matplotlib.pyplot as plt

### Configuracao serial Agilent 34401A - Senis
##serAg2 = serial.Serial(4)
##serAg2.baudrate = 9600
##serAg2.bytesize = serial.EIGHTBITS
##serAg2.stopbits = serial.STOPBITS_ONE
##serAg2.parity = serial.PARITY_NONE
##serAg2.timeout = .063
##if not serAg2.isOpen():
##    serAg2.open()
##
### Configuracao serial NMR
##serNMR = serial.Serial(5)
##serNMR.baudrate = 19200
##serNMR.bytesize = serial.EIGHTBITS
##serNMR.stopbits = serial.STOPBITS_ONE
##serNMR.parity = serial.PARITY_NONE
##serNMR.timeout = .015
##if not serNMR.isOpen():
##    serNMR.open()
##
##
###Configuracao Serial Agilent 34970A - Temperatura Bloco
##serAg = serial.Serial(6)
##serAg.baudrate = 9600
##serAg.bytesize = serial.EIGHTBITS
##serAg.stopbits = serial.STOPBITS_ONE
##serAg.parity = serial.PARITY_NONE
##serAg.timeout = 0.001
##if not serAg.isOpen():
##    serAg.open()
## 
##
### Configuracao serial Group3
##serG3 = serial.Serial(7)
##serG3.baudrate = 9600
##serG3.bytesize = serial.EIGHTBITS
##serG3.stopbits = serial.STOPBITS_TWO
##serG3.parity = serial.PARITY_NONE
##serG3.timeout = 0.05
##if not serG3.isOpen():
##    serG3.open()


# Comandos NMR
LerCampo = '\x05'
Status = 'S1'
Manual = 'A0'
Auto = 'A1'
Remoto = 'R'
Local = 'L'
Canal = 'PD'
Coarse = 'C1410\r\n'
Display = 'D1'


#Comandos Agilent
Acessar = 'SYST:REM\r\n'
Limpar = '*CLS\r\n'
Resetar = '*RST\r\n'
LerAg = 'READ?\r\n'


#Comandos Agilent 34970A
VConf = 'CONF:TEMP RTD,85,(@101:104)\r\n'
ResisA = 'SENS:TEMP:TRAN:RTD:RES:REF 99.981,(@101)\r\n'
ResisB = 'SENS:TEMP:TRAN:RTD:RES:REF 100.0272,(@102)\r\n'
ResisC = 'SENS:TEMP:TRAN:RTD:RES:REF 99.955,(@103)\r\n'
ResisD = 'SENS:TEMP:TRAN:RTD:RES:REF 100.047,(@104)\r\n'
Resis = 'SENS:TEMP:TRAN:RTD:RES:REF 100,(@101:104)\r\n'
Scan = 'ROUT:SCAN (@101:104)\r\n'
Ncanais = 4


#Comandos Agilent 34401A
VConf2 = ':CONF:VOLT:DC 10,0.00003\r\n'


# Comandos Group3
Acessa = 'A1\r'
Filtro = 'D0\r'
Escala = 'R1\r'
Unidade = 'UFG\r'
LerTemp = 'T'
LerCampoG3 = 'F'


########################### Configurações Instrumentação ######################


#Definições Agilent 34970
def AcessarVolt():
    serAg.write(Acessar.encode('utf-8'))

def LimparVolt():
    serAg.write(Limpar.encode('utf-8'))

def ResetarVolt():
    serAg.write(Resetar.encode('utf-8'))

def ConfigurarVolt():
    serAg.write(VConf.encode('utf-8'))
    serAg.write(Scan.encode('utf-8'))
    time.sleep(0.165)
    serAg.write(ResisA.encode('utf-8'))
    time.sleep(0.165)
    serAg.write(ResisB.encode('utf-8'))
    time.sleep(0.165)
    serAg.write(ResisC.encode('utf-8'))
    time.sleep(0.165)
    serAg.write(ResisD.encode('utf-8'))
    time.sleep(0.165)
    serAg.write(Resis.encode('utf-8'))
    serAg.write(Scan.encode('utf-8'))
    
    
def LerVolt():
    serAg.write(LerAg.encode('utf-8'))
    time.sleep(0.25)
    ValorStr = serAg.read(100).decode('utf-8')
    ValorStr = re.sub('\n','',ValorStr)
    ValorStr = re.sub('\r','',ValorStr)
    valor = ValorStr.split(',')
    return valor

def teste():
    Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
    Datahora = str(Datahora)
    print(Datahora)
    a=0
    b=0
    c=0
    d=0
    serAg.write(LerAg.encode('utf-8'))
    time.sleep(0.07)
    a=serAg.read(64).decode('utf-8')
    time.sleep(0.056)
    b=serAg.read(64).decode('utf-8')
    time.sleep(0.056)
    c=serAg.read(64).decode('utf-8')
    time.sleep(0.056)
    d=serAg.read(64).decode('utf-8')
    print('*'+a+'*')
    print('*'+b+'*')
    print('*'+c+'*')
    print('*'+d+'*')
    Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
    Datahora = str(Datahora)
    print(Datahora+'\n')

def CommandsVolt():
    AcessarVolt()
    LimparVolt()
    ResetarVolt()
    ConfigurarVolt()


#Definições Agilent 34401 - Campo Senis
def AcessarVolt2():
    serAg2.write(Acessar.encode('utf-8'))

def LimparVolt2():
    serAg2.write(Limpar.encode('utf-8'))

def ResetarVolt2():
    serAg2.write(Resetar.encode('utf-8'))

def ConfigurarVolt2():
    serAg2.write(VConf2.encode('utf-8'))
##    serAg2.write('DISP OFF\r\n'.encode('utf-8'))
    
def LerVolt2():
    serAg2.write(LerAg.encode('utf-8'))
    ValorStr = serAg2.read(20).decode('utf-8')
    ValorStr = re.sub('\n','',ValorStr)
    ValorStr = re.sub('\r','',ValorStr)
    ValorStr = re.sub('C','',ValorStr)
    valor = ConvFloat(ValorStr)
##    valor = ValorStr
    return valor
    
def CommandsVolt2():
    AcessarVolt2()
    LimparVolt2()
    ResetarVolt2()
    ConfigurarVolt2()

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


#Definições Group3

def EscreverG3(Comando):
    serG3.write(Comando.encode('utf-8'))

def Ler():
    return serG3.read(20)

def ConfiguraG3():
    EscreverG3(Acessa)
    EscreverG3(Filtro)
    EscreverG3(Escala)
    EscreverG3(Unidade)

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
        EscreverG3(LerCampoG3)
        ValorStr = Ler()
        # Trata variavel
        ValorStr = ValorStr.decode('utf-8')
        ValorStr = re.sub('\n','',ValorStr)
        ValorStr = re.sub('\r','',ValorStr)
        ValorStr = re.sub('G','',ValorStr)
        valor = float(ValorStr)

    return valor


############################Configurações Iniciais#############################

def Config():
    CommandsVolt()
    CommandsVolt2()
##    ConfiguraNMR()
    ConfiguraG3()
    
###################################Rotinas#####################################

def ConvFloat(valorStr):
    try:
        valor = float(valorStr)
    except:
        valor = 0
    return valor


def LerLoop(npontos):
    # Criar lista vazia
    listacampoNMR = np.array([])
    listacampoG3 = np.array([])
    listastatusNMR = np.array([])
    listadatahora = np.array([])
    listatempB = []

    conta = 0
##    tempB =  LerVolt()
  
    for i in range(npontos):
        a = LerCampoNMR()
        status = a[0]
        campoNMR = float(a[1:])*10000
        tempB = LerVolt()
        campoG3 = LerG3(1)
        Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
        Datahora = str(Datahora)
        listacampoNMR = np.append(listacampoNMR,campoNMR)
        listacampoG3 = np.append(listacampoG3,campoG3)
        listastatusNMR = np.append(listastatusNMR,status)
        listadatahora = np.append(listadatahora,Datahora)
        listatempB.append([])
        for j in range (Ncanais):
            listatempB[i].append(tempB[j])
        campoNMR = '{0:.3f}'.format(campoNMR)
        tempB[0] = '{0:.3f}'.format(float(tempB[0]))
        tempB[1] = '{0:.3f}'.format(float(tempB[1]))
        tempB[2] = '{0:.3f}'.format(float(tempB[2]))
        tempB[3] = '{0:.3f}'.format(float(tempB[3]))
        print('{} Data-Hora = {}\t Campo NMR[G] = {}  {}\t Campo G3[G] = {}\t Temp Bloco[°C] =   a -> {}    b -> {}    c -> {}    d -> {}'.format(i+1,Datahora,status,campoNMR,campoG3,tempB[0],tempB[1],tempB[2],tempB[3]))
        time.sleep(59.66)
        if conta == 100:
            conta = 0
            SalvaArqs(listadatahora,listastatusNMR,listacampoNMR,listacampoG3,listatempB)
        conta = conta + 1

    a = len(listatempB)
    for i in range (a):
        for j in range (Ncanais):
            listatempB[i][j] = float(listatempB[i][j])
    SalvaArqs(listadatahora,listastatusNMR,listacampoNMR,listacampoG3,listatempB)


def LerLoop2(npontos):
    # Criar lista vazia
    listacampoSe = np.array([])
    listacampoG3 = np.array([])
    listadatahora = np.array([])
    listatempB = []

    conta = 0
##    tempB =  LerVolt()
  
    for i in range(npontos):
        campoSe =  (LerVolt2()/0.0005)
        tempB = LerVolt()
        campoG3 = LerG3(1)
        Datahora = time.strftime("%d/%m/%Y %H:%M:%S")
        Datahora = str(Datahora)
        listacampoSe = np.append(listacampoSe,campoSe)
        listacampoG3 = np.append(listacampoG3,campoG3)
        listadatahora = np.append(listadatahora,Datahora)
        listatempB.append([])
        for j in range (Ncanais):
            listatempB[i].append(tempB[j])
        campoSe = '{0:.3f}'.format(campoSe)
        campoG3 = '{0:.2f}'.format(campoG3)
        tempB[0] = '{0:.3f}'.format(float(tempB[0]))
        tempB[1] = '{0:.3f}'.format(float(tempB[1]))
        tempB[2] = '{0:.3f}'.format(float(tempB[2]))
        tempB[3] = '{0:.3f}'.format(float(tempB[3]))
        print('{} Data-Hora = {}\t Campo Se[G] = {}\t Campo G3[G] = {}\t Temp Bloco[°C] =   a -> {}    b -> {}    c -> {}    d -> {}'.format(i+1,Datahora,campoSe,campoG3,tempB[0],tempB[1],tempB[2],tempB[3]))
        time.sleep(59.67)
        if conta == 100:
            conta = 0
            SalvaArqs2(listadatahora,listacampoSe,listacampoG3,listatempB)
        conta = conta + 1

    a = len(listatempB)
    for i in range (a):
        for j in range (Ncanais):
            listatempB[i][j] = float(listatempB[i][j])
    SalvaArqs2(listadatahora,listacampoSe,listacampoG3,listatempB)


def GeraGraf(dados,dados2):
    plt.plot(dados)
    plt.plot(dados2)
    plt.show()


def SalvaArqs(D0,D1,D2,D3,D4):
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','w')
    f.close()
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','a')
    tamanho = len(D1)
    for i in range (tamanho):
        f.write(D0[i]+'\t'+str(D1[i])+'\t'+str(D2[i])+'\t'+str(D3[i])+'\t'+str(D4[i][0])+'\t'+str(D4[i][1])+'\t'+str(D4[i][2])+'\t'+str(D4[i][3])+'\n')
    f.close()

def SalvaArqs2(D1,D2,D3,D4):
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','w')
    f.close()
    f = open('D:\ARQ\Ariane\Teste\Saida2.txt','a')
    tamanho = len(D1)
    for i in range (tamanho):
        f.write(D1[i]+'\t'+str(D2[i])+'\t'+str(D3[i])+'\t'+str(D4[i][0])+'\t'+str(D4[i][1])+'\t'+str(D4[i][2])+'\t'+str(D4[i][3])+'\n')
    f.close()

def testelista():
    a = []
    for i in range(3):
        a.append([])
        for j in range(3):
            a[i].append(i+j)
    print(a)
