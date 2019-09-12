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

from Escalonador import *
from Eventos import *
from Fel import *

import sys
import argparse

#import cProfile

#def main():
    #cProfile.run(statement='run()', filename='saida-v3.cprof')


def main():
    # Método de escalonamento ("FCFS", "RR"...).
    escalonador = None
    # Arquivo de cenario ("cenarioD1.txt").
    cenario = None
    # Modo probabilístico ou determinístico ("P" ou "D").
    modo = None
    # Valor de quantum do escaloador Round Robin.
    quantum = None

    parser = argparse.ArgumentParser()
    parser.add_argument('escalonador', metavar='scheduler', type=str, help='método de escalonamento')
    parser.add_argument('quantum', metavar='quantum', type=int, help='valor de quantum')
    parser.add_argument('arquivo', metavar='file', type=str, help='arquivo contendo o cenário')
    parser.add_argument('modo', metavar='mode', type=str, help='modo probabilístico ou determinístico')
    args = vars(parser.parse_args())

    escalonador = RR(args['quantum'])
    cenario = args['arquivo']
    modo = args['modo']

    run(escalonador, cenario, modo)


def run(escalonador, cenario, modo):

    fel = Fel(escalonador, cenario, modo)

    if modo == 'D':
        while len(fel.getFel()) > 0:
            fel.consome()

    elif modo == 'P':
        while fel.getTempo() < fel.eventos.tempoSimulacao:
            fel.consome()

    fel.fimExecucao()


if __name__ == "__main__":
    main()
