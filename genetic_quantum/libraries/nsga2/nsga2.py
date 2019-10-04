#!/usr/bin/env python3

################################################################################
#                                                                              #
#  NSGA-II: Non-dominated Sorting Genetic Algorithm II                         #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Contact: Thales Otávio | @ThalesORP | ThalesORP@gmail.com                   #
#                                                                              #
################################################################################

'''Main class of NSGA-II.'''

import matplotlib.pyplot as plt # pylint: disable=import-error
import numpy as np # pylint: disable=import-error

from .population import Population

class NSGA2():
    '''Main class of the NSGA-II algorithm.'''

    def __init__(self, generations, population_size, offspring_size):
        self.generations = generations
        self.population_size = population_size
        self.offspring_size = offspring_size

        self.population = Population(self.population_size, self.offspring_size)

    # Methods
    def run(self):
        '''Method responsible for running the main loop of NSGA2.
        Starts with one population of size "population_size".
        It's created the children of this population, that will be the quantity of "offspring_size".
        The creation of those children is made by crossover and mutation.
        Sort them with: non-dominated sorting.
        Take the best individual according with: crowding distance sorting.
        "population_size" is the max size of the new population.
        Back to beginning. Repeated N generations.'''
        self.initiate_population()

        for generation in range(self.generations):

            print("\nGENERATION:", generation+1)

            #self.population._show_individuals() # pylint: disable=protected-access

            print("NON DOMINATED SORTING...")
            self.non_dominated_sorting()

            print("CROWDING DISTANCE SORTING...")
            self.crowding_distance_sorting()

            print("CROSSOVER...")
            self.crossover()

            print("MUTATION...")
            self.mutation()

            #self.population._show_individuals() # pylint: disable=protected-access

            print("EVALUATING INDIVIDUALS...")
            self.evaluate()

            input()

    def initiate_population(self):
        ''' Initiate the population of NSGA-II.'''
        self.population.initiate()
        print("EVALUATING INDIVIDUALS...")
        self.evaluate()

    def non_dominated_sorting(self):
        ''' Sort the individuals according to they dominance and sort them into fronts.

        Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual.
        Also, the first front is created.
        Then the remaining individuals are divided into fronts.'''
        self.population.reset_fronts()

        self.population.new_front()

        # Each of individuals checks if dominates or is dominated with everyone else.
        for i in range(self.population_size):
            for j in range(self.population_size):
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
        ''' Crowding distance sorting algorithm.
        Reject the fronts that doesn't fit in the population of next generation.
        Find the crowding distance value for each individual.
        Sort them in they front with this value.
        Discard the individuals that doesn't fit on new population.'''

        # Rejecting the fronts that doesn't fit in the population for next generation.
        individual_quantity = 0
        quantity_of_fronts = 0

        for front in self.population.fronts:
            # Checking if the quantity of individuals exceeded the limit, wich is offspring_size.
            if individual_quantity >= self.offspring_size:
                quantity_of_fronts += 1
            else:
                individual_quantity += len(front)

        while quantity_of_fronts != 0:
            self.population.delete_last_front()
            quantity_of_fronts -= 1


        # Calculating the crowding distance value for each individual.

        solutions_amount = len(front[0].solutions)

        for front in self.population.fronts:
            # List of lists: solutions_lists has "solutions_amount" lists. For example:
            # solutions_lists = [ [1, 3], [24.6, 14.4], [746, 324] ]
            # Each list is a objective function value. In that way, 1, 24.6 and 746
            # is the solutions of the first individual, and 3, 14.4 and 324 is of
            # the second individual.
            solutions_lists = list()

            for i in range(solutions_amount):
                solutions_list = list()
                for individual in front:
                    solutions_list.append(individual.solutions[i])
                solutions_lists.append(solutions_list)


            # Getting the data and making the calculation of crowding distance for each individual.
            for i in range(len(front)):
                individual = front[i]

                # Getting the index of current individual.
                individual_index = i

                # If there is only one individual in that front,
                if len(front) == 1:
                    # there's no need to calculate their crowding distance.
                    continue

                # Usually, the value is as described bellow.
                left_neighbour_index = individual_index - 1
                right_neighbour_index = individual_index + 1

                # But when isn't, then it's checked the cases when there's no neighbour on one side.
                if individual_index == 0:
                    # When it happens, the closest neighbour it's himself.
                    left_neighbour_index = 0
                elif individual_index == (len(solutions_list)-1):
                    right_neighbour_index = (len(solutions_list)-1)

                # Summation of crowding distance of each objective function.
                for solutions_list in solutions_lists:
                    right_neighbour_value = solutions_list[right_neighbour_index]
                    left_neighbour_value = solutions_list[left_neighbour_index]

                    max_value = max(solutions_list)
                    min_value = min(solutions_list)

                    individual.crowding_distance += ((right_neighbour_value - left_neighbour_value)
                                                     / (max_value - min_value))

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

        # Getting the quantity of individuals that are needed to create.
        amount_to_create = self.population_size - len(self.population.individuals)

        child_chromosome_list = list()

        for _ in range(amount_to_create):
            first_parent = self.population.get_random_individual()
            second_parent = self.population.get_random_individual()

            child_chromosome = (first_parent.chromosome + second_parent.chromosome) // 2

            child_chromosome_list.append(child_chromosome)

        for child_chromosome in child_chromosome_list:
            self.population.new_individual(child_chromosome)

    def mutation(self):
        '''Mutation method.'''
        '''Dicidir quantos indivíduos vão sofrer mutação.
        Sortear X% conforme a aplitude. (population.chromosome_max_value, population.chromosome_min_value)
        Sortear se será acresentado ou subtraído tal porcentagem do quantum do individuo.'''

    def evaluate(self):
        '''How the individuals are evaluated.'''

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
        plt.xticks(np.arange(self.X_MIN_VALUE, self.X_MAX_VALUE+1, 5.0))
        plt.yticks(np.arange(self.Y_MIN_VALUE, self.Y_MAX_VALUE+1, 5.0))

        plt.title('Individual fronts')
        chartBox = ax.get_position()
        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
        ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

        #plt.legend(loc='upper left')
        plt.show()
