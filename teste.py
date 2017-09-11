#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Created on 12/2014
Versão 1.0
@author: Lucas Igor Balthazar
"""
#Importa bibliotecas
import serial
import Agilent_3458A
import time
import sys

b=Agilent_3458A.GPIB()

def Conectar(Addr):
    try:
        return b.Conectar(Addr)
    except:
        return False

def confgs(aperture,timer):
    try:
        return b.Config(aperture,timer)
    except:
        return False
