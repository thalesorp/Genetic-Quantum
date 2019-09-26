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
from .load import Cenario
from .cpu import CPU
from .dispositivo import Dispositivo
from .processo import Processo

class Colecoes():
    ''' Class docstring.'''

    def __init__(self):
        self.CPUs = []
        self.Dispositivos = []
        self.Processos = []
        self.Finalizados = []
        self.nProcessos = 0

    # Retorna a Primeira CPU livre que encontrar na coleção.
    def buscaCpuLivre(self):
        for cpu in self.CPUs:
            if cpu.getDisponivel():
                return cpu
        else:
            return None

    def buscaCpu(self, ident):
        for cpu in self.CPUs:
            if cpu.getCpuId() == ident:
                return cpu

        return None

    def buscaDispositivo(self, ident):
        for dispositivo in self.Dispositivos:
            if dispositivo.getDispositivoId() == ident:
                return dispositivo
                
        return None

    def buscaProcesso(self, ident):

        '''
        print(" - ")
        for processo in self.Processos:
            print(processo)
        print(" - ")
        '''

        for processo in self.Processos:
            if processo.getProcessoId() == ident:
                return processo
        return None

    def finalizaProcesso(self, ident):
        for i in range(len(self.Processos)):
            if self.Processos[i].getProcessoId() == ident:
                self.Finalizados.append(self.Processos[i])
                del self.Processos[i]
                return
        return
