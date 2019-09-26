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

class Fila():
    ''' Uma classe para manipular listas como fila.'''

    def __init__(self):
        self.queue = list()

    def insert(self, element):
        ''' Method docstring.'''
        self.queue.append(element)

    def remove(self, ident=None):
        ''' Method docstring.'''
        if not self.empty():
            if ident is None:
                head = self.queue[0]
                del self.queue[0]
                return head
            for processo in self.queue:
                if processo.getProcessoId() == ident:
                    pos = self.queue.index(processo)
                    del self.queue[pos]
        else:
            return "Empty queue."

    def empty(self):
        ''' Method docstring.'''
        if not self.queue:
            # Empty queue.
            return True
        return False

    def toString(self):
        ''' Method docstring.'''
        temp = ""

        for element in self.queue:
            temp = temp + str(element) + '\n'

        return temp
