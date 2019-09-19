#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
#                                                                              #
#  Genetic quantum                                                             #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Contact:                                                                    #
#    Thales Otávio | @ThalesORP | ThalesORP@gmail.com                          #
#                                                                              #
################################################################################

'''Root class of this project.'''

from libraries.nsga2.nsga2 import NSGA2 # pylint: disable=import-error
from libraries.simpro.simpro import SimPro

class GeneticQantum(NSGA2):
    ''' Main class of this project.'''

    GENERATIONS = 5
    POPULATION_SIZE = 20
    OFFSPRING_SIZE = 10

    def __init__(self):
        # Calling the parent constructor.
        super().__init__(self.GENERATIONS, self.POPULATION_SIZE, self.OFFSPRING_SIZE)
        self.simulator = SimPro()

    def run(self):
        '''Method responsible for calling the NSGA-II.'''
        super().run()
    
    def runSimPro(self):
        quantum = 5
        # Path to scenario file ("probabilistic_scenario_1.txt").
        scenario = "resources/scenarios/probabilistic/probabilistic_scenario_1.txt"
        # Probabilistic or deterministic mode ("P" or "D").
        modo = "P"
        self.simulator.run(quantum, scenario)
