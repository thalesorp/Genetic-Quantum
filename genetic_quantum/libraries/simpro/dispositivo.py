#!/usr/bin/env python3

################################################################################
#                                                                              #
#  SimPro:                                                                     #
#    Simulador de escalonamento de processos                                   #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Orientador: Diego Mello Silva                                               #
#  Aluno: Danilo da Silva Alves                                                #
#                                                                              #
################################################################################

''' Module docstring.'''

from .fila import Fila

class Dispositivo():
    ''' Class docstring.'''

    def __init__(self, ident):
        self.filaIO = Fila()
        self.processoAtual = 0
        self.disponivel = True
        self.dispositivoId = ident

    def setDispositivoId(self, ident):
        self.dispositivoId = ident

    def getDispositivoId(self):
        return self.dispositivoId

    def setProcessoAtual(self, processo):
        self.processoAtual = processo

    def getProcessoAtual(self):
        return self.processoAtual

    def setDisponivel(self, flag):
        self.disponivel = flag

    def getDisponivel(self):
        return self.disponivel
