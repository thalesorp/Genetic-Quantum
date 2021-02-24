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

from .eventos import Evento
import sys

class Fel():
    ''' Class docstring.'''

    def __init__(self, escalonador, cenario, modelo):
        self.fel = []
        self.tempo = 0
        self.eventoId = 0

        self.eventos = Evento(escalonador, cenario, modelo)
        lista_eventos = self.eventos.start()

        self.agenda_evento(lista_eventos)

    def agenda_evento(self, lista_eventos):
        ''' Agenda o evento.'''

        for evento in lista_eventos:
            pos = 0
            self.eventoId += 1

            if not self.fel:
                # Caso a FEL esteja vazia.
                self.fel.append(evento)
            elif evento[0] == 0:
                self.fel.insert(0, evento)
            else:
                # Enquanto o tempo do evento for maior, percorre FEL.
                for evento_agendado in self.fel:
                    if evento_agendado[1] > evento[1]:
                        break
                    else:
                        pos = pos + 1

                self.fel.insert(pos, evento)

    def desagenda_evento(self, processoId, cpuId):
        ''' Desagenda Evento. '''
        for i in range(len(self.fel)):
            evento = self.fel[i]
            # Buscando execução agendada.
            if evento[0] == 2:
                if evento[2] == processoId and evento[3] == cpuId:
                    del self.fel[i]
                    return

    def consome(self):
        ''' Consome o próximo evento da FEL.'''
        evento = self.proximo_evento()
        self.remove_primeiro_evento()
        lista_eventos = []

        if evento[0] == 0:
            # Desagendar algum evento da FEL.
            processoId = evento[1]
            cpuId = evento[2]
            self.desagenda_evento(processoId, cpuId)
        else:
            self.tempo = evento[1]
            processoId = evento[2]

            if evento[0] == 1:
                lista_eventos = self.eventos.fimChegadaProcessoCPU(self.tempo, processoId)

            elif evento[0] == 2:
                cpuId = evento[3]
                lista_eventos = self.eventos.fimExecutaCPU(self.tempo, processoId, cpuId)

            elif evento[0] == 3:
                lista_eventos = self.eventos.fimExecutaIO(self.tempo, processoId)

            elif evento[0] == 4:
                lista_eventos = self.eventos.fimEncerraProcesso(self.tempo, processoId)

            self.agenda_evento(lista_eventos)

    def remove_primeiro_evento(self):
        ''' Method docstring.'''
        del self.fel[0]

    def proximo_evento(self):
        ''' Se a FEL não estiver vazia, retornar o primeiro elemento dela.'''
        #if len(self.fel) > 0:
        if self.fel:
            return self.fel[0]

        # Se ela estiver vazia, terminar a execução.
        sys.exit()

    def fim_execucao(self):
        ''' Method docstring.'''
        self.eventos.fim_execucao(self.tempo)
