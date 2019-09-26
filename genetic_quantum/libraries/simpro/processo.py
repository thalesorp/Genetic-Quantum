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

import random

class Processo():
    ''' Class docstring.'''

    def __init__(
            self, ident, quantum, nIOdist, ioBurstDist, cpuBurstDist,
            dispositivoId, chegada, prioridade, lista=None):

        self.inicioExecucao = 0.0
        self.terminoExecucao = 0.0

        # Variável para controlar o tempo de execução total.
        self.tempoExecucao = 0.0

        # Variável para controlar o tempo de espera total.
        self.tempoEspera = 0.0

        self.cpuBursts = []
        self.ioBursts = []
        self.nIoBursts = 0
        self.nCpuBursts = 0

        self.dPrioridade = 0.0
        self.rri = 0.0
        self.processoId = 0

        # Determinístico.
        if lista is not None:
            # [identificador][chegada][burst][prioridade]
            self.setProcessoId(lista[0])
            self.nCpuBursts = 1
            self.chegada = lista[1]
            self.cpuBursts.append(lista[2])
            self.prioridade = lista[3]
            self.setQuantum(quantum)
            self.tempoAuxiliar = self.chegada
        # Probabilístico.
        else:
            self.tempoAuxiliar = chegada
            self.chegada = chegada

            self.setProcessoId(ident)

            # Prioridade estática.
            self.prioridade = int(random.triangular(prioridade[0], prioridade[2], prioridade[1]))

            self.setQuantum(quantum)

            if (nIOdist[0] == 0) and (nIOdist[1] == 0) and (nIOdist[2] == 0):
                self.nIoBursts = 0
            else:
                self.nIoBursts = int(random.triangular(nIOdist[0], nIOdist[2], nIOdist[1]))

            self.nCpuBursts = self.nIoBursts + 1

            self.setDispositivo(dispositivoId)

            for _ in range(self.nCpuBursts):
                self.cpuBursts.append(int(random.triangular(cpuBurstDist[0], cpuBurstDist[2], cpuBurstDist[1])))

            for _ in range(self.nIoBursts):
                self.ioBursts.append(int(random.triangular(ioBurstDist[0], ioBurstDist[2], ioBurstDist[1])))

        print("-> nCpuBursts:", self.nCpuBursts, "\tcpuBursts:", self.cpuBursts, "\tprocessoId:", self.processoId)

        self.dicionarioExecucao = []

    def setRri(self, valor):
        ''' Method docstring.'''
        self.rri = valor

    def getRri(self):
        ''' Method docstring.'''
        return self.rri

    def getBursts(self):
        ''' Method docstring.'''
        return self.cpuBursts

    def getExecucoes(self):
        ''' Method docstring.'''
        return self.dicionarioExecucao

    def insereExecucao(self):
        ''' Method docstring.'''
        nome = "p" + str(self.getProcessoId())

        tempoI = self.converteTempo(self.getInicioExecucao())
        tempoT = self.converteTempo(self.getTerminoExecucao())

        inicio = '2018-01-01 ' + tempoI
        termino = '2018-01-01 ' + tempoT
        self.dicionarioExecucao.append([nome, inicio, termino])

    def recalculaExecucao(self):
        ''' Method docstring.'''
        self.dicionarioExecucao[(len(self.dicionarioExecucao)-1):][0][2] = '2018-01-01 ' + self.converteTempo(self.getTerminoExecucao())

    def getTempoExecucao(self):
        ''' Method docstring.'''
        return self.tempoExecucao

    def incExecucao(self, tempo):
        ''' Method docstring.'''
        self.tempoExecucao += (tempo - self.tempoAuxiliar)
        self.tempoAuxiliar = tempo

    def getTempoEspera(self):
        ''' Method docstring.'''
        return self.tempoEspera

    def setAuxiliar(self, tempo):
        ''' Method docstring.'''
        self.tempoAuxiliar = tempo

    def incEspera(self, tempo):
        ''' Method docstring.'''
        self.tempoEspera += (tempo - self.tempoAuxiliar)
        self.tempoAuxiliar = tempo

    def getPrioridade(self):
        ''' Method docstring.'''
        return self.prioridade

    def setPrioridadeDinamica(self, dpi):
        ''' Method docstring.'''
        self.dPrioridade = dpi

    def getPrioridadeDinamica(self):
        ''' Method docstring.'''
        return self.dPrioridade

    def setTerminoExecucao(self, tempo):
        ''' Method docstring.'''
        self.terminoExecucao = tempo

    def getTerminoExecucao(self):
        ''' Method docstring.'''
        return self.terminoExecucao

    def getChegada(self):
        ''' Method docstring.'''
        return self.chegada

    def setInicioExecucao(self, tempo):
        ''' Method docstring.'''
        self.inicioExecucao = tempo

    def getInicioExecucao(self):
        ''' Method docstring.'''
        return self.inicioExecucao

    def setProcessoId(self, ident):
        ''' Method docstring.'''
        self.processoId = ident

    def getProcessoId(self):
        ''' Method docstring.'''
        return self.processoId

    def getnCpuBursts(self):
        ''' Method docstring.'''
        return self.nCpuBursts

    def getnIoBursts(self):
        ''' Method docstring.'''
        return self.nIoBursts

    def setQuantum(self, quantum):
        ''' Method docstring.'''
        self.quantum = quantum

    def getQuantum(self):
        ''' Method docstring.'''
        return self.quantum

    def decrementaIoBursts(self):
        ''' Method docstring.'''
        del self.ioBursts[0]
        self.nIoBursts -= 1

    def decrementaCpuBursts(self):
        ''' Method docstring.'''
        del self.cpuBursts[0]
        self.nCpuBursts -= 1

    def getIoBurstAtual(self):
        ''' Method docstring.'''
        return self.ioBursts[0]

    def getCpuBurstAtual(self):
        ''' Method docstring.'''
        return self.cpuBursts[0]

    def setDispositivo(self, disp):
        ''' Method docstring.'''
        self.dispositivoId = disp

    def getDispositivo(self):
        ''' Method docstring.'''
        return self.dispositivoId

    def reduzCpuBurst(self, valor):
        ''' Method docstring.'''
        tempo = valor - self.getInicioExecucao()

        self.cpuBursts[0] -= tempo

    def subQuantum(self):
        ''' Method docstring.'''

        print("nCpuBursts:", self.nCpuBursts, "\tcpuBursts:", self.cpuBursts, "\tprocessoId:", self.processoId)
        if self.quantum >= self.cpuBursts[0]:                                   # <--- "IndexError: list index out of range". A lista CpuBursts está vazia.
            self.decrementaCpuBursts()
            return False
        else:
            self.cpuBursts[0] -= self.quantum
            #print('Reduziu: ', self.cpuBursts[0])
            return True

    def converteTempo(self, tempo):
        ''' Method docstring.'''
        t1 = int(tempo%60) #00:00:[00]
        aux = int(tempo/60)
        if  aux < 60:
            t2 = aux #00:[00]:00
            t3 = 00
        else:
            t2 = aux/60
            t3 = aux%60

        if t1<10:
            st1 = '0'+str(t1)
        else:
            st1 = str(t1)

        if t2<10:
            st2 = '0'+str(t2)
        else:
            st2 = str(t2)

        if t3<10:
            st3 = '0'+str(t3)
        else:
            st3 = str(t3)

        t = st3+':'+st2+':'+st1
        return t
