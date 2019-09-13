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

'''Main class of NSGA-II.'''

import sys
import random

import matplotlib.pyplot as plt
import numpy as np

from .population import Population

class NSGA2:
    '''Main class of the NSGA-II algorithm.'''

    # Attributes
    POPULATION_SIZE = 10
    OFFSPRING_SIZE = 5

    X_MIN_VALUE = 0
    X_MAX_VALUE = 100

    Y_MIN_VALUE = 0
    Y_MAX_VALUE = 100

    GENERATIONS = 10

    # Constructor
    def __init__(self):
        random.seed(3)

        self.population = Population(
            self.POPULATION_SIZE, self.OFFSPRING_SIZE,
            self.X_MIN_VALUE, self.X_MAX_VALUE,
            self.Y_MIN_VALUE, self.Y_MAX_VALUE)

    # Methods
    def run(self):
        '''Method responsible for running the main loop of NSGA2.'''

        '''Starts with one population of size 'POPULATION_SIZE'.
        It's created the children of this population, that will be the quantity of 'OFFSPRING_SIZE'.
        The creation of those children is made by crossover and mutation.
        Sort them with: non-dominated sorting.
        Take the best individual according with: crowding distance sorting.
        'POPULATION_SIZE' is the max size of the new population.
        Back to beginning. Repeated N generations.''' # pylint: disable=pointless-string-statement

        self.population.start_new_population()

        print("GENERATION: 0")
        #self._plot_individuals()
        #input()

        for gen in range(self.GENERATIONS):

            print("GENERATION:", gen+1)

            '''print("\n-> BEFORE NON DOMINATED SORTING:")
            self.population._show_fronts()
            self.population._show_individuals()'''

            self.non_dominated_sorting()

            print("\n-> BEFORE CROWDING DISTANCE SORTING:")
            self.population._show_fronts()
            self.population._show_individuals()
            print("")
            print("len(self.population.fronts):", len(self.population.fronts))
            self.crowding_distance_sorting()

            '''print("\n-> BEFORE CROSSOVER:")
            self.population._show_fronts()
            self.population._show_individuals()'''

            self.crossover()

            self.mutation()

            '''print("\n-> BEFORE START NEW GENERATION:")
            self.population._show_fronts()
            self.population._show_individuals()'''

            #self._plot_individuals_fronts()

            input()

    def non_dominated_sorting(self):
        '''Sort the individuals according to they dominance and sort them into fronts.'''

        '''Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual.
        Also, the first front is created.
        Then the remaining individuals are divided into fronts.''' # pylint: disable=pointless-string-statement

        self.population.reset_fronts()

        self.population.new_front()

        # Each of individuals checks if dominates or is dominated with everyone else.
        for i in range(self.POPULATION_SIZE):
            for j in range(self.POPULATION_SIZE):
                current_individual = self.population.individuals[i]
                other_individual = self.population.individuals[j]

                if i != j: # Ignoring itself.
                    # Checking if dominates or are dominated by the other individuals.
                    if current_individual.dominates(other_individual):
                        current_individual.dominated_by.append(other_individual)
                    elif other_individual.dominates(current_individual):
                        current_individual.domination_count += 1

            current_front = self.population.get_last_front()
            # Checking if current individual is eligible to the first front.
            if current_individual.domination_count == 0:
                if current_individual not in current_front:
                    self.population.add_to_last_front(current_individual)

        # Temporary list with the current front.
        current_front = list()

        i = 0
        while len(self.population.fronts[i]) > 0: # pylint: disable=len-as-condition
            self.population.new_front()
            for individual in self.population.fronts[i]:
                for dominated_individual in individual.dominated_by:
                    dominated_individual.domination_count -= 1
                    # Now if this dominated individual aren't dominated by anyone,
                        # insert into next front.
                    if dominated_individual.domination_count == 0:
                        self.population.add_to_last_front(dominated_individual)
            i += 1

        # Deleting empty last front created in previously loops.
        self.population.delete_last_front()

    def crowding_distance_sorting(self):
        '''Crowding distance sorting algorithm.'''

        '''Reject the fronts that doesn't fit in the population of next generation.
        Find the crowding distance value for each individual.
        Sort them in they front with this value.
        Discard the individuals that doesn't fit on new population.'''

        # Rejecting the fronts that doesn't fit in the population for next generation.

        individual_quantity = 0
        quantity_of_fronts = 0

        for front in self.population.fronts:
            # Checking if the quantity of individuals exceeded the limit, wich is OFFSPRING_SIZE.
            if individual_quantity >= self.OFFSPRING_SIZE:
                quantity_of_fronts += 1
            else:
                individual_quantity += len(front)

        print("Rejected fronts:", quantity_of_fronts)

        while quantity_of_fronts != 0:
            self.population.delete_last_front()
            quantity_of_fronts -= 1

        i = 1
        print("len(self.population.fronts):", len(self.population.fronts))
        # Calculating the crowding distance value for each individual.
        for front in self.population.fronts:
            print("Front", i)
            i += 1
            # Temporary lists that holds the x and y values of current front.
            x_values = list()
            y_values = list()

            for individual in front:
                x_values.append(individual.x_value)
                y_values.append(individual.y_value)
            x_values.sort()
            y_values.sort()

            min_x_value = min(x_values)
            max_x_value = max(x_values)
            min_y_value = min(y_values)
            max_y_value = max(y_values)

            # Getting the data and making the calculation of crowding distance for each individual.
            for individual in front:
                # Getting the index of current individual on the x and y values lists.
                x_index = x_values.index(individual.x_value)
                y_index = y_values.index(individual.y_value)

                # X:
                # Checking if there's only one individual in that front.
                if len(x_values) == 1:
                    # When this happens, he's the left and right neighbour of yourself.
                    x_value_left_neighbour = x_values[0]
                    x_value_right_neighbour = x_values[0]
                else:
                    # Usually, the value is as described bellow.
                    x_left_neighbour_index = x_index - 1
                    x_right_neighbour_index = x_index + 1
                    # But when isn't, then it's checked the cases when there's no neighbour on one side.
                    if x_index == 0:
                        # When it happens, the closest neighbour it's himself.
                        x_left_neighbour_index = 0
                    elif x_index == (len(x_values)-1):
                        x_right_neighbour_index = (len(x_values)-1)
                    # Getting the value of neighbours, which is what matters.
                    x_value_left_neighbour = x_values[x_left_neighbour_index]
                    x_value_right_neighbour = x_values[x_right_neighbour_index]

                # Y:
                if len(y_values) == 1:
                    y_value_top_neighbour = y_values[0]
                    y_value_bottom_neighbour = y_values[0]
                else:
                    y_top_neighbour_index = y_index + 1
                    y_bottom_neighbour_index = y_index - 1

                    if y_index == 0:
                        y_bottom_neighbour_index = 0
                    elif y_index == (len(y_values)-1):
                        y_top_neighbour_index = (len(y_values)-1)

                    y_value_top_neighbour = y_values[y_top_neighbour_index]
                    y_value_bottom_neighbour = y_values[y_bottom_neighbour_index]


                individual.crowding_distance += ((x_value_right_neighbour - x_value_left_neighbour)
                                                 / (max_x_value - min_x_value)) #<--- Division by zero!

                individual.crowding_distance += ((y_value_top_neighbour - y_value_bottom_neighbour)
                                                 / (max_y_value - min_y_value)) #<--- Division by zero!


        self.population.sort_fronts_by_crowding_distance()


        # Getting the amount of individuals to delete, and removing them.

        # Getting the sum of individuals from all fronts but the last.
        individual_counter = 0
        for i in range(0, len(self.population.fronts)-1):
            individual_counter += len(self.population.fronts[i])

        # Quantity of individuals of last front that will continue to next generation.
        remaining_individuals = self.population.offspring_size - individual_counter

        # Getting the front that will have individuals removed.
        last_front = self.population.get_last_front()

        # Getting the amount of individuals that are gonna be removed.
        amount_to_remove = len(last_front) - remaining_individuals

        # Deleting the last "amount_to_remove" individuals from last front.
        while amount_to_remove != 0:
            individual = last_front[len(last_front)-1]
            self.population.delete_individual_from_last_front(individual)
            amount_to_remove -= 1

    def crossover(self):
        '''Crossover method.'''
        population_current_size = self.population.get_current_population_size()

        individual_remaining = self.POPULATION_SIZE - population_current_size

        # Creating new individuals from two random individuals.
        for _ in range(individual_remaining):

            parent_one = self.population.get_random_individual()
            parent_two = self.population.get_random_individual()

            if (random.random() % 2) == 0:
                x_value = parent_one.x_value
                y_value = parent_two.y_value
            else:
                x_value = parent_two.x_value
                y_value = parent_one.y_value

            self.population.new_individual(x_value, y_value)

    def mutation(self):
        '''Mutation method.'''
        pass

    # Plotting
    def _plot_individuals(self):
        x_values = list()
        y_values = list()

        for individual in self.population.individuals:
            x_values.append(individual.x_value)
            y_values.append(individual.y_value)

        ax = plt.subplot(111)

        plt.plot(x_values, y_values, "ko", label="individuals")

        plt.axis([self.X_MIN_VALUE, self.X_MAX_VALUE, self.Y_MIN_VALUE, self.Y_MAX_VALUE])
        plt.xticks(np.arange(self.X_MIN_VALUE, self.X_MAX_VALUE+1, 1.0))
        plt.yticks(np.arange(self.Y_MIN_VALUE, self.Y_MAX_VALUE+1, 1.0))

        plt.title('Individual fronts')
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

        plt.show()

    def _plot_individuals_fronts(self):
        multiple_x_values = list()
        multiple_y_values = list()
        x_values = list()
        y_values = list()

        for front in self.population.fronts:
            x_values = list()
            y_values = list()
            for individual in front:
                x_values.append(individual.x_value)
                y_values.append(individual.y_value)
            multiple_x_values.append(x_values)
            multiple_y_values.append(y_values)

        #colors = ['go','ro','bo', 'mo', 'yo', 'co', 'no', 'ko']
        colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo',
                  'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo',
                  'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo',
                  'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo',
                  'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo',
                  'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo',
                  'bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko', 'wo']
        labels = ['Front 1', 'Front 2', 'Front 3', 'Front 4', 'Front 5',
                  'Front 6', 'Front 7', 'Front 8', 'Front 9', 'Front 10',
                  'Front 11', 'Front 12', 'Front 13', 'Front 14', 'Front 15',
                  'Front 16', 'Front 17', 'Front 18', 'Front 19', 'Front 20',
                  'Front 21', 'Front 22', 'Front 23', 'Front 24', 'Front 25',
                  'Front 26', 'Front 27', 'Front 28', 'Front 29', 'Front 30']

        ax = plt.subplot(111)

        i = 0
        for i in range(len(multiple_x_values)):
            plt.plot(multiple_x_values[i], multiple_y_values[i], colors[i], label=labels[i])

        #plt.plot(self.x_values, self.y_values, 'ro')
        #plt.plot(self.x_values, self.y_values, 'ro')

        plt.axis([self.X_MIN_VALUE, self.X_MAX_VALUE, self.Y_MIN_VALUE, self.Y_MAX_VALUE])
        plt.xticks(np.arange(self.X_MIN_VALUE, self.X_MAX_VALUE+1, 1.0))
        plt.yticks(np.arange(self.Y_MIN_VALUE, self.Y_MAX_VALUE+1, 1.0))

        plt.title('Individual fronts')
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

        #plt.legend(loc='upper left')
        plt.show()

    # Utils
    def sort_individuals(self, individual_list):
        '''Sort an list of individuals.'''

        sum_list = list()
        xy_sum = 0
        for individual in individual_list:
            xy_sum = individual.x_value + individual.y_value
            sum_list.append(xy_sum)

        lowest = None
        for i in range(len(individual_list)):
            # Finding the lowest value.
            lowest_index = 0
            lowest = sum_list[0]
            for j in range(1, len(sum_list)):
                if sum_list[j] < lowest:
                    lowest_index = j
                    lowest = sum_list[j]

            # Remove an element from list by index.
            sum_list.pop(lowest_index)
            lowest = individual_list.pop(lowest_index)
            # Insert the lowest to the first available position.
            sum_list.insert(0, sys.maxsize)
            individual_list.insert(i, lowest)

    def _show_individuals_from_list(self, individual_list):
        for individual in individual_list:
            sys.stdout.write(str(individual) + ', ')
        print()
