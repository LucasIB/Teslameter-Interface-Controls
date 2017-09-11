# -*- coding: utf-8 -*-
"""
Created on 01/07/2013
Versão 3.0
@author: James Citadini
"""
# Importa bibliotecas
import time
import visa
import threading
import ctypes
import numpy as np
# ******************************************

class GPIB(object):
    def __init__(self):
        try:
            self.Comandos()
        except:
            return None

    def Conectar(self,address):
        try:
            aux = 'GPIB0::'+str(address)
            self.inst = visa.instrument(aux.encode('utf-8'))
            self.inst.timeout = 1

            return self.Enviar('RESET')
        except:
            return False
    def Comandos(self):
        pass
       
    def Enviar(self,comando):
        try:
            self.inst.write(comando)
            return True
        except:
            return False

    def Ler(self):
        try:
            leitura = self.inst.read()
        except:
            leitura = ''

        return leitura

    def Ler_Volt(self):
        try:
            leitura = float(self.inst.read())
        except:
            leitura = ''

        return leitura
    
    def Config(self,aperture,timer):
        try:
             #Configuração do voltímetro Agilent 3458A
            self.Enviar('RESET')                # Permite definir o multímetro para o estado power-on, sem executar o cilco de ligação.
            self.Enviar('DCV 10')               # DV VOLTAGE, 10V range.
            self.Enviar('TARM AUTO')            # Define o evento que permite o evento de disparo (TRIG comando). Também pode-se usar este comando para executar a medição de múltiplos ciclos.
            self.Enviar('TRIG AUTO')            # Trigger Automático.
            self.Enviar('EXTOUT OFF')           # Especifica o evento que gera um sinal na parte traseira conector do painel Ext Out (sinal EXTOUT). RCOMP: Leitura completa (Pulso de 1E-06 depois de cada leitura). POS: gera um sinal TTL positivo.
            self.Enviar('SCRATCH')              # Limpa todos os subprogramas e estados de armazenamento da memória.
            self.Enviar('DELAY 0')              # O comando DELAY permite que você especifique um intervalo de tempo que é inserido entre o TRIGGER e o SAMPLE.
            self.Enviar('APER '+str(aperture))  # Especifica o tempo de integração do conversor A / D em segundos.
            self.Enviar('TIMER '+str(timer))    # Seleciona o tempo em segundos do intervalo de SAMPLES.
            self.Enviar('NRDGS 1,TIMER')        # 1 leitura por sample event (TIMER).
            self.Enviar('NDIG 6')               # Números de dígitos habilitado.
            self.Enviar('MATH OFF')             # O comando MATH ativa ou desativa as operações matemáticas em tempo real.
            self.Enviar('AZERO ONCE')           # Ativa ou desativa a função autozero. ONCE: Medição Zero é atualizado uma vez após qqr função realizada.
            self.Enviar('DISP ON')              # Ativa ou desativa o Display do multímetro. ON: Ativado.
            self.Enviar('END 2')                # O comando END habilita ou desabilita o Fim GPIB ou a função identificar (EOI). END 2: Linha EOI envia True quando o último byte de cada leitura é enviado.
            self.Enviar('TBUFF OFF')            # Trigger Buffer: Ativa ou desativa o buffer de disparo externo do multímetro. 
            self.Enviar('MEM OFF')              # Para leituras de armazenamento (leituras armazenadas permanecem intactas).
            self.Enviar('MEM FIFO')             # Permite a leitura da memória. FIFO: Apaga a memória de leitura e armazena novas leituras. FIFO (first-in-first-out).
            return True
        except:
            return False


    def Config_Single(self,aperture,timer):
        try:
             #Configuração do voltímetro Agilent 3458A
            self.Enviar('RESET')
            self.Enviar('DCV 10')
            self.Enviar('TARM SYN')
            self.Enviar('TRIG SYN')
            self.Enviar('EXTOUT OFF')
            self.Enviar('SCRATCH')            
            self.Enviar('DELAY 0')
            self.Enviar('NDIG 6')
            self.Enviar('MATH OFF')
            self.Enviar('AZERO ONCE')
            self.Enviar('DISP ON')
            self.Enviar('APER '+str(aperture))
            self.Enviar('TIMER '+str(timer))
            self.Enviar('NRDGS 1')
            self.Enviar('MEM OFF')
            self.Enviar('END 2')
            self.Enviar('TBUFF OFF')
            return True
        except:
            return False


    def DescarregaVoltimetro(self):
        try:
            # Verifica numero de pontos na memoria        
            self.Enviar('MCOUNT?')
            ValorMem = int(self.Ler())
            if ValorMem == 0:
                raise Exception()

            # Inicia retirada dos dados da memoria
            self.Enviar('RMEM 1,'+ str(ValorMem))

            leituras = ''
            for i in range(int(ValorMem)):
                leituras = leituras + self.Ler()
                
            # Separa elementos
            tmp = leituras.split(',')

            #Converte para float
            dados = [float(x) for x in tmp]
        except:
            dados = []

        return dados
     
