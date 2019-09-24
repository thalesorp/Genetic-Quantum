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

import os

#from Escalonador import *
from .escalonador import Escalonador, RR
#from Eventos import *
from .eventos import Evento
from .fel import Fel

#from .population import Population

import sys
import argparse

class SimPro(object):

    def run(self, quantum, scenario, mode):
        #print("\nIn \"SimPro\"...")
        #print("  Quantum:", quantum)
        #print("  Scenario:", scenario)
        #print("  Mode:", mode)

        scheduler = RR(quantum)

        fel = Fel(scheduler, scenario, mode)

        if mode == 'D':
            while len(fel.getFel()) > 0:
                fel.consome()

        elif mode == 'P':
            while fel.getTempo() < fel.eventos.tempoSimulacao:
                fel.consome()

        fel.fimExecucao()

    def run_and_get_results(self, quantum):
        ''' Return one list with all four results of simulation.'''
        self.run_SimPro(quantum)
        #print("rodou o run_SimPro(quantum)")
        return self.get_last_SimPro_result()

    def run_SimPro(self, quantum):
        quantum = quantum
        # Path to scenario file ("probabilistic_scenario_1.txt").
        scenario = "resources/scenarios/probabilistic/probabilistic_scenario_1.txt"
        #scenario = "resources/scenarios/deterministic/deterministic_scenario_2.txt"
        # Probabilistic or deterministic mode ("P" or "D").
        modo = "P"
        #modo = "D"
        #print("self.run(",quantum ,",", scenario ,",", modo,")")
        self.run(quantum, scenario, modo)

    def get_SimPro_results(self):
        #pasta: /media/thalesorp/Baphomet/Projects/GitHub/Genetic-Quantum/genetic_quantum/resources/SimPro-results
        root_path = os.getcwd()
        #directories_up = 3
        #for _ in range(directories_up):
            #root_path = root_path[:root_path.rfind('/')]
        results_folder = root_path + "/resources/SimPro-results"
        result_file = results_folder + "/RR.txt"
        #print("result_file:", result_file)

        with open(result_file) as f:
            # Getting from the second line to last.
            for line in islice(f, 1, None):
                # Removing "\n" in the end of line.
                line = line.rstrip()
                # Putting the values into a list.
                line = line.split("\t")
                print("line:", line)

    def get_last_SimPro_result(self):
        root_path = os.getcwd()
        results_folder = root_path + "/resources/SimPro-results"
        result_file = results_folder + "/RR.txt"

        with open(result_file) as f:
            for line in f:
                pass

        # Removing "\n" in the end of line.
        line = line.rstrip()
        # Putting the values into a list.
        line = line.split("\t")
        # Converting all values to int, because split turn them to string.
        line = [ float(value) for value in line ]

        return line


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

#import cProfile

#def main():
    #cProfile.run(statement='run()', filename='saida-v3.cprof')

if __name__ == "__main__":
    main()
