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

class Population:
    '''Class of population of indiviuals, used by NSGA-II.'''

    # Attributes

    # Constructor
    def __init__(
            self, population_size, offspring_size,
            x_min_value, x_max_value,
            y_min_value, y_max_value):

        self.population_size = population_size
        self.offspring_size = offspring_size
        self.x_min_value = x_min_value
        self.x_max_value = x_max_value
        self.y_min_value = y_min_value
        self.y_max_value = y_max_value

        #self.current_size = None

        random.seed(3)

        self.individuals = list()

        # List with all fronts.
        self.fronts = list()

        self.offspring = list()

        # Used to plot the individuals.
        #self.x_values = list()
        #self.y_values = list()

    # Methods
    def start_new_population(self):
        '''Initialize a new population.'''

        names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'

        for i in range(self.population_size):
            x_value = random.randint(self.x_min_value, self.x_max_value)
            #self.x_values.append(x_value)

            y_value = random.randint(self.y_min_value, self.y_max_value)
            #self.y_values.append(y_value)

            new_individual = Individual(names[i], x_value, y_value)
            self.individuals.append(new_individual)

    def sort_fronts_by_crowding_distance(self):
        '''Sort the current fronts by the crowding distance value in ascending order.'''
        for front in self.fronts:
            front.sort(key=lambda x: x.crowding_distance, reverse=True)

    def get_current_population_size(self):
        amount = 0
        for front in self.fronts:
            amount += len(front)
        return amount

    def get_random_individual(self):
        population_current_size = self.get_current_population_size()
        counter = random.randint(1, population_current_size-1)

        for front in self.fronts:
            for individual in front:
                if counter == 0:
                    return individual
                counter -= 1

    def new_individual(self, x_value, y_value):
        new_individual = Individual("A", x_value, y_value)
        self.individuals.append(new_individual)

    def organize_for_new_generation(self):
        ''' Putting all individuals sorted in fronts to individuals list.'''
        for front in self.fronts:
            for individual in front:
                self.individuals.append(individual)
                front.remove(individual)
        self.front = list()
        print("Front:", self.front)

    # Utils
    def _show_population(self):
        '''Show the x and y values of each individual of population.'''
        for individual in self.individuals:
            sys.stdout.write(str(individual) + ", ")
            #print(individual)

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
        i = 1
        for front in self.fronts:
            sys.stdout.write("Front " + str(i) + ": ")
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
