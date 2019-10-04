#!/usr/bin/env python3

################################################################################
#                                                                              #
#  Genetic quantum:                                                            #
#    Finding the best quantum to Round-robin scheduling with NSGA-II.          #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Contact: Thales Otávio | @ThalesORP | ThalesORP@gmail.com                   #
#                                                                              #
################################################################################

''' Module docstring.'''

from libraries.nsga2.nsga2 import NSGA2 # pylint: disable=import-error,no-absolute-import
from libraries.simpro.simpro import SimPro # pylint: disable=import-error

class GeneticQantum(NSGA2):
    ''' Main class of this project.'''

    GENERATIONS = 5
    POPULATION_SIZE = 10
    OFFSPRING_SIZE = 5

    def __init__(self):
        # Calling the parent constructor.
        super().__init__(self.GENERATIONS, self.POPULATION_SIZE, self.OFFSPRING_SIZE)
        self.simulator = SimPro()

    # NSGA-II.
    def evaluate(self):
        '''How the individuals are evaluated.'''

        i = 0
        for individual in self.population.individuals:
            # Checking if individual already has solutions.
            if not individual.solutions:

                quantum = individual.chromosome

                individual.solutions = self.simulator.run_and_get_results(quantum)

                i += 1
                result = "  [" + str(i) + "]\t" + str(individual)
                #print(result+"\n\n\n")

                '''new_individual = Individual(quantum)
                new_individual.solutions = self.simulator.run_and_get_results(quantum)

                result = "  [" + str(i) + "]\t" + str(new_individual)
                print(result+"\n\n\n")'''

    def evaluate_individual(self, individual):
        '''Evaluating one single individual.'''

        quantum = individual.chromosome
        individual.solutions = self.simulator.run_and_get_results(quantum)
