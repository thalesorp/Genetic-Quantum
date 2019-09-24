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

from .eventos import Evento
import sys

class Fel(object):

    fel = None
    tempo = None
    eventos = None
    eventoId = None

    def __init__(self,escalonador,cenario,modelo):
        self.fel = []
        self.tempo = 0.0
        self.eventoId = 0
    
        self.eventos = Evento(escalonador, cenario, modelo)
        agendar = self.eventos.start() 

        self.agendaEvento(agendar)

    def getTempo(self):
        return self.tempo

    def setTempo(self, tempo):
        self.tempo = tempo

    def getFel(self):
        return self.fel

    #Agenda o evento
    def agendaEvento(self, listaEventos):
        #print '----LISTA PARA AGENDAR------'
        #print listaEventos
        if len(listaEventos) > 0:
            for evento in listaEventos:
                pos = 0
                self.eventoId += 1 
                if(len(self.fel) == 0): #Caso a fel esteja vazia
                    self.fel.append(evento)
                elif evento[0] == 0:
                    self.fel.insert(0,evento)
                else:
                    for eventoAgendado in self.fel: #Enquanto o tempo do evento for maior, percorre FEL
                        if(evento[1] < eventoAgendado[1]):
                            break
                        else:
                            pos = pos + 1
                    self.fel.insert(pos, evento)
        else:
            pass
        #print 'Agendado'

    def desagenda_evento(self, processoId, cpuId):
        ''' Desagenda Evento. '''
        '''for i in range(len(self.fel)):
            evento = self.fel[i]
            # Buscando execução agendada.
            if evento[0] == 2: 
                if evento[2] == processoId:
                    if evento[3] == cpuId:
                        self.fel.pop(i)
                        break'''
        for evento in self.fel:
            # Buscando execução agendada.
            if evento[0] == 2: 
                if (evento[2] == processoId) and (evento[3] == cpuId):
                    del self.fel[i]
                    return

    def consome(self):
        ''' Consome o próximo evento da FEL. '''
        evento = self.proximo_evento()
        self.remove_primeiro_evento()
        lista_eventos = []

        # Fim da chegada de processos na CPU. (?)
        if evento[0] == 1:
            self.tempo = evento[1]
            processoId = evento[2]
            lista_eventos = self.eventos.fimChegadaProcessoCPU(self.tempo, processoId)
            self.agendaEvento(lista_eventos)

        # Fim da execução na CPU.
        elif evento[0] == 2:
            self.tempo = evento[1]
            processoId = evento[2]
            cpuId = evento[3]
            lista_eventos = self.eventos.fimExecutaCPU(self.tempo, processoId, cpuId)
            self.agendaEvento(lista_eventos)

        elif evento[0] == 3: #fimExecutaIO(self,tempo,processo)#
            self.tempo = evento[1]
            lista_eventos = self.eventos.fimExecutaIO(self.getTempo(),evento[2])
            #print 'Fim execucao IO'
            self.agendaEvento(lista_eventos)

        elif (evento[0] == 4):#fimEncerraProcesso(self,tempo,processo)#
            self.tempo = evento[1]
            processoId = evento[2]
            lista_eventos = self.eventos.fimEncerraProcesso(self.tempo, processoId)
            self.agendaEvento(lista_eventos)

        # Desagendar algum evento da FEL.
        elif (evento[0] == 0):
            processoId = evento[1]
            cpuId = evento[2]
            self.desagenda_evento(processoId, cpuId)

    def remove_primeiro_evento(self):
        del self.fel[0]

    def proximo_evento(self):
        # Se a FEL não estiver vazia, retornar o primeiro elemento dela.
        if len(self.fel) > 0:
            return self.fel[0]
        
        # Se ela estiver vazia, terminar a execução.
        sys.exit()

    def fimExecucao(self):
        #print 'Chamar Fim EVENTO'
        self.eventos.fimExecucao(self.getTempo())

    def toString(self):
        pass
        #1 - Chegada de processo
        #2 - Execução na CPU
        #3 - Execução IO
        #4 - Fim de execucao
