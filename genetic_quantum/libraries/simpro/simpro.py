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

import os
import sys
import argparse

from .escalonador import RR
from .eventos import Evento
from .fel import Fel

class SimPro():
    ''' Root class of SimPro.'''

    def run(self, quantum, scenario):
        ''' Run the simulation with minimum requirements to execute RR scheduler.'''

        scheduler = RR(quantum)
        fel = Fel(scheduler, scenario, "D")

        while fel.fel:
            fel.consome()

        fel.fim_execucao()

    def get_last_result(self, scenario):
        ''' Method docstring.'''

        root_path = os.getcwd()
        results_folder = root_path + "\\resources\\SimPro-results\\"

        scenario_name = str(scenario).rsplit('/', 1)[1].rsplit('.', 1)[0]

        result_file_name = results_folder + scenario_name + "_results.txt"

        with open(result_file_name) as f:
            for line in f:
                pass

        # Removing "\n" in the end of line.
        line = line.rstrip()
        # Putting the values into a list.
        line = line.split("\t")
        # Converting all values to int, because split turn them to string.
        line = [float(value) for value in line]

        return line

################################################################################

# DEPRECATED
'''
    def get_simpro_results(self):

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
    '''
''' DEPRECATED
def main():

    # Método de escalonamento ("FCFS", "RR"...).
    escalonador = None
    # Arquivo de cenario ("cenarioD1.txt").
    cenario = None
    # Modo probabilístico ou determinístico ("P" ou "D").
    modo = None
    parser = argparse.ArgumentParser()
    parser.add_argument('escalonador', metavar='scheduler', type=str, help='método de escalonamento')
    parser.add_argument('quantum', metavar='quantum', type=int, help='valor de quantum')
    parser.add_argument('arquivo', metavar='file', type=str, help='arquivo contendo o cenário')
    parser.add_argument('modo', metavar='mode', type=str, help='modo probabilístico ou determinístico')
    args = vars(parser.parse_args())
    escalonador = RR(args['quantum'])
    cenario = args['arquivo']
    modo = args['modo']
    #run(escalonador, cenario, modo)

#import cProfile

#def main():
    #cProfile.run(statement='run()', filename='saida-v3.cprof')

if __name__ == "__main__":
    main()
'''