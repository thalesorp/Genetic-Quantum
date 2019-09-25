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

import os
from itertools import islice

from libraries.nsga2.nsga2 import NSGA2 # pylint: disable=import-error
from libraries.nsga2.individual import Individual
from libraries.simpro.simpro import SimPro

class GeneticQantum(NSGA2):
    ''' Main class of this project.'''

    GENERATIONS = 5
    POPULATION_SIZE = 10
    OFFSPRING_SIZE = 5

    def __init__(self):
        # Calling the parent constructor.
        super().__init__(self.GENERATIONS, self.POPULATION_SIZE, self.OFFSPRING_SIZE)
        #self.simulator = SimPro()

    '''
    def run(self):
        ''''''Method responsible for calling the NSGA-II.''''''
        self.initiate_population()

        for generation in range(self.GENERATIONS):

            print("GENERATION:", generation+1)

            self.non_dominated_sorting()

            self.crowding_distance_sorting()

            self.crossover()

            self.mutation()
    '''

    # NSGA-II.
    def evaluate(self):
        '''How the individuals are evaluated.'''

        simulator = SimPro()

        i = 1
        for individual in self.population.individuals:
            # Checking if individual already has solutions.
            if not individual.solutions:
                quantum = individual.chromosome
                print("Quantum to evaluate:", quantum)
                
                individual.solutions = simulator.run_and_get_results(quantum)

                result = "  [" + str(i) + "]\t" + str(individual)
                print(result+"\n\n\n")

                new_individual = Individual(quantum)
                new_individual.solutions = simulator.run_and_get_results(quantum)
                
                result = "  [" + str(i) + "]\t" + str(new_individual)
                print(result+"\n\n\n")

                i += 1

    def evaluate_individual(self, individual):
        print("Evaluating single individual...")

        simulator = SimPro()

        quantum = individual.chromosome
        individual.solutions = simulator.run_and_get_results(quantum)
        print(individual)
