#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
#                                                                              #
#  NSGA-II: Non-dominated Sorting Genetic Algorithm II                         #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Contact:                                                                    #
#    Thales Otávio | @ThalesORP | ThalesORP@gmail.com                          #
#                                                                              #
################################################################################

'''File of population class.'''

import sys
import random

from .individual import Individual

class Population(object):
    '''Class of population of indiviuals, used by NSGA-II.'''

    # Constructor
    def __init__(self, population_size, offspring_size):
        random.seed(1)

        self.population_size = population_size
        self.offspring_size = offspring_size

        self.chromosome_min_value = 0
        self.chromosome_max_value = 100

        self.individuals = list()

        # List with all fronts: each front contains the indexes of the individuals in "self.individuals".
        self.fronts = list()

    # Methods
    def initiate(self):
        ''' Initialize a new population.'''
        for _ in range(self.population_size):
            chromosome = random.randrange(self.chromosome_min_value, self.chromosome_max_value)
            self.new_individual(chromosome)

    def new_individual(self, chromosome):
        ''' Insert a new individual into population.'''
        self.individuals.append(Individual(chromosome))

    # Front utils
    def reset_fronts(self):
        ''' Reset all fronts, i. e., delete all previous fronts.'''
        self.fronts = list()

    def new_front(self):
        ''' Start a new front.'''
        self.fronts.append([])

    def sort_fronts_by_crowding_distance(self):
        '''Sort the current fronts by the crowding distance value in ascending order.'''
        for front in self.fronts:
            front.sort(key=lambda x: x.crowding_distance, reverse=True)

    #^ Ok.

    def get_random_individual(self):
        ''' Return a random individual of this population.'''
        population_current_size = self.get_current_population_size()
        counter = random.randrange(1, population_current_size-1)

        for front in self.fronts:
            for individual in front:
                if counter == 0:
                    return individual
                counter -= 1

    def add_to_front(self, index, individual):
        ''' Add the individual into "index" front.'''
        self.fronts[index].append(individual)

    def add_to_last_front(self, individual):
        ''' Add individual to last front.'''
        #index = self.individuals.index(individual)
        #self.fronts[self.get_last_front_index()].append(index)
        self.fronts[self.get_last_front_index()].append(individual)

    def get_last_front(self):
        ''' Return the last front.'''
        return self.fronts[len(self.fronts)-1]

    def delete_individual_from_last_front(self, individual):
        ''' Deletes the individual from front AND from individuals list.'''

        # Deleting from last front the individual with index = "index".
        last_front = self.get_last_front()
        index = last_front.index(individual)
        del last_front[index]

        # Deletng from individuals list.
        self.individuals.remove(individual)

    def delete_last_front(self):
        '''Deleting the last front and the individuals inside.'''
        last_front = self.get_last_front()
        for individual in last_front:
            self.individuals.remove(individual)
        self.fronts.remove(last_front)

    # Utils
    def _show_population(self):
        '''Show the x and y values of each individual of population.'''
        for individual in self.individuals:
            sys.stdout.write(str(individual) + ", ")
            #print(individual)

    def _show_individuals(self):
        '''Show the x and y values of each individual of population.'''
        sys.stdout.write("INDIVIDUALS:\n  ")
        for individual in self.individuals:
            sys.stdout.write(str(individual) + ", ")
        print("")

    def _show_general_domination_info(self):
        '''Show all data of population.'''
        for individual in self.individuals:
            sys.stdout.write("  Individual: " + str(individual)
                             + "\tdomination count: " + str(individual.domination_count)
                             + "\tdominated by this: ")
            for dominated_individual in individual.dominated_by:
                sys.stdout.write(str(dominated_individual.name) + ", ")
            print("")
        print("")

    def _show_fronts(self):
        '''Show all fronts.'''
        print("FRONTS:")

        i = 1
        for front in self.fronts:
            sys.stdout.write("  Front " + str(i) + ": ")
            i += 1
            for individual in front:
                sys.stdout.write(str(individual) + ", ")
            print("")

    def _show_fronts_with_crowding_distance(self):
        '''Show all fronts.'''
        i = 1
        for front in self.fronts:
            sys.stdout.write("Front " + str(i) + ": ")
            i += 1
            for individual in front:
                sys.stdout.write(str(individual) + ".CD: " + str(individual.crowding_distance) + ", ")
            print("")

    def _show_offspring(self):
        '''Show individuals of the offspring.'''
        print("\nOffspring:")
        for individual in self.offspring:
            sys.stdout.write(str(individual) + ", ")
        print("")

    def _show_individuals_from_list(self, individual_list):
        for individual in individual_list:
            sys.stdout.write(str(individual) + ', ')

    # Debug
    def start_new_population_debug(self):
        '''DEBUG: Initialize a new population.'''
        self.population = list()

        individual = Individual('A', 3, 3)
        self.population.append(individual)

        individual = Individual('B', 4, 2)
        self.population.append(individual)

        individual = Individual('C', 1, 2)
        self.population.append(individual)

        individual = Individual('D', 1, 1)
        self.population.append(individual)

        individual = Individual('E', 2, 1)
        self.population.append(individual)

        individual = Individual('F', 3, 2)
        self.population.append(individual)
