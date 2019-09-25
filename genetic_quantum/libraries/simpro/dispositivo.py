#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------#
#         Graduação em Ciência da Computação           #
#                                                      #
#    Orientador: Diego Mello Silva                     #
#    Aluno: Danilo da Silva Alves                      #
#    Matrícula: 0002749                                #
#                                                      #
#------------------------------------------------------#

from .fila import Fila

class Dispositivo(object):

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
