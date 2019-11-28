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

import matplotlib.pyplot as plt
import numpy as np
import random
import imageio
import os
# Used to get "sys.maxsize", the pseudo infinite.
import sys

from .population import Population

class NSGA2():
    '''Main class of the NSGA-II algorithm.'''

    # "ZDT1", "ZDT2", "GQ".
    TEST_PROBLEM = "ZDT1"

    GENERATIONS = 250

    # "N" on NSGA-II paper.
    POPULATION_SIZE = 100

    # Distribution index. "nc" in NSGA-II paper.
    CROSSOVER_CONSTANT = 30

    # Crossover probability. "pc" in NSGA-II paper.
    CROSSOVER_RATE = 0.9

    # Size of genome list. For Genetic Quantum, this value must be 1.
    GENOTYPE_QUANTITY = 30

    GENOME_MIN_VALUE = 0
    GENOME_MAX_VALUE = 1

    # Mutation probability. "pm" in NSGA-II paper.
    MUTATION_RATE = 1/GENOTYPE_QUANTITY

    # Percentage of chance to disturbing one genotype of genome.
    GENOTYPE_MUTATION_PROBABILITY  = 0.5

    # Percentage to disturb each genotype mutated.
    DISTURB_PERCENT = 50

    def __init__(self):
        # "Rt" on NSGA-II paper.
        self.population = Population(self.GENOTYPE_QUANTITY, self.GENOME_MIN_VALUE, self.GENOME_MAX_VALUE)

    def run(self):
        '''Method responsible for running the main loop of NSGA-II.'''

        print("GENERATION 0")

        # Creating a parent population P0.
        self.initiate_population()

        fronts = self.fast_non_dominated_sort()
        #self._show_fronts(fronts)

        # "Q0" on NSGA-II paper.
        offspring_population = self.usual_crossover()
        self.evaluate(offspring_population)

        for i in range(self.GENERATIONS):
            print("GENERATION", i+1)

            # "Rt" population: union between "Pt" and "Qt", now with size of "2N".
            self.population.union(offspring_population)

            # "F" on NSGA-II paper.
            fronts = self.fast_non_dominated_sort()
            #self._show_fronts(fronts)

            self._save_plot(i+1, fronts)

            self.crowding_distance_assignment(fronts)

            # "Pt+1" population.
            next_population = self.new_population()

            i = 0
            while (next_population.size + fronts[i].size) <= self.POPULATION_SIZE:
                next_population.union(fronts[i])
                i += 1

            # Sort(Fi, <n)
            self.sort_by_crowded_comparison(fronts[i])

            # "Pt+1" = "Pt+1" union fronts[i][1 : "N" - sizeof("Pt+1")]
            amount_to_insert = self.POPULATION_SIZE - len(next_population.individuals)
            fronts[i].individuals = fronts[i].individuals[:amount_to_insert]
            next_population.union(fronts[i])

            self.population = next_population

            # Make new offspring population. "Qt+1" on NSGA-II paper.
            offspring_population = self.crossover()
            self.evaluate(offspring_population)

        self._generate_gif()

    def new_population(self):
        ''' Return a empty Population object.'''

        return Population(self.GENOTYPE_QUANTITY, self.GENOME_MIN_VALUE, self.GENOME_MAX_VALUE)

    def initiate_population(self):
        ''' Initiate the population of NSGA-II.'''

        self.population.initiate(self.POPULATION_SIZE//2)
        self.evaluate(self.population)

    def fast_non_dominated_sort(self):
        ''' Sort the individuals according to they dominance and sort them into fronts.
        Everyone check with everyone who dominates who, filling up
        "domination_count" and "dominated_by" attributes of each individual.
        Also, the first front is created.
        Then the remaining individuals are divided into fronts.'''

        self.population.reset_fronts()

        # Initializing the fronts list and the first front.
        fronts = list()
        fronts.append(self.new_population())

        # Each of individuals checks if dominates or is dominated with everyone else.
        for i in range(self.population.size):
            for j in range(self.population.size):
                current_individual = self.population.individuals[i]
                other_individual = self.population.individuals[j]

                if i != j: # Ignoring itself.
                    # Checking if dominates or are dominated by the other individuals.
                    if current_individual.dominates(other_individual):
                        current_individual.dominated_by.append(other_individual)
                    elif other_individual.dominates(current_individual):
                        current_individual.domination_count += 1

            # Checking if current individual is eligible to the first front.
            if current_individual.domination_count == 0:
                if current_individual not in fronts[0].individuals:
                    current_individual.rank = 1
                    fronts[0].insert(current_individual)

        # Temporary front.
        current_front = self.new_population()

        i = 0
        while len(fronts[i].individuals) > 0:
            fronts.append(self.new_population())
            for individual in fronts[i].individuals:
                for dominated_individual in individual.dominated_by:
                    dominated_individual.domination_count -= 1

                    # Now if this dominated individual aren't dominated by anyone, insert into next front.
                    if dominated_individual.domination_count == 0:

                        # "+1" becasue "i" is index value, and rank starts from 1 and not 0.
                        # "+1" because the rank it's for the next front.
                        dominated_individual.rank = i+2
                        fronts[len(fronts)-1].insert(dominated_individual)
            i += 1

        # Deleting empty last front created in previously loops.
        del fronts[len(fronts)-1]

        return fronts

    def crowding_distance_assignment(self, fronts):
        ''' Calculates the crowding distance value of each individual.'''

        for population in fronts:

            last_individual_index = len(population.individuals)-1

            # Reseting this value because it's a new generation.
            for individual in population.individuals:
                individual.crowding_distance = 0

            '''# If the population has only one individual, he receives the "infinite" value of crowding distance.
            if population.size == 1:
                population.individuals[0].crowding_distance = sys.maxsize
                print("IN CROWDING DISTANCE CALCULATION: Only one individual!")
                #continue'''

            for genome_index in range(self.GENOTYPE_QUANTITY):

                # Sorting current population (front) according to the current objective (genome).
                population.individuals.sort(key=lambda x: x.genome[genome_index])

                # The first and last individuals of current population (front) receive "infinite".
                population.individuals[0].crowding_distance = sys.maxsize
                population.individuals[last_individual_index].crowding_distance = sys.maxsize

                min_value, max_value = population.get_extreme_neighbours(genome_index)

                # Calculating the crowding distance of each objective (genome) of all individuals.
                for i in range(1, last_individual_index):
                    right_neighbour_value = population.individuals[i+1].genome[genome_index]
                    left_neighbour_value = population.individuals[i-1].genome[genome_index]

                    # population.individuals[i].crowding_distance += ((right_neighbour_value - left_neighbour_value) / (max_value - min_value))
                    if (max_value - min_value) == 0:
                        print("IN CROWDING DISTANCE: division by zero!")
                        population.individuals[i].crowding_distance += ((right_neighbour_value - left_neighbour_value) / 1)
                    else:
                        population.individuals[i].crowding_distance += ((right_neighbour_value - left_neighbour_value) / (max_value - min_value))

    def crowded_comparison(self, individual_A, individual_B):
        ''' Return the best individual according to the crowded comparison operator
        in NSGA-II paper.'''

        if ((individual_A.rank < individual_B.rank)
            or ((individual_A == individual_B)
            and (individual_A.crowding_distance > individual_B.crowding_distance))):
            return individual_A
        return individual_B

    def sort_by_crowded_comparison(self, population):
        ''' Sort "population" with crowded comparison operator. Bubble sort.'''

        for i in range(len(population.individuals)-2):

            worst = population.individuals[i]

            for j in range(1, len(population.individuals)-i):

                worst = self.crowded_comparison(worst, population.individuals[j])

            population.individuals.remove(worst)
            population.individuals.append(worst)

        worst = population.individuals[0]
        population.individuals.remove(worst)
        population.individuals.append(worst)

    def tournament_selection(self):
        ''' Binary tournament selection according to crowded comparison operator.'''

        first_candidate = self.population.get_random_individual()
        second_candidate = self.population.get_random_individual()

        return self.crowded_comparison(first_candidate, second_candidate)

    def usual_tournament_selection(self):
        ''' Usual binary tournament selection.'''

        first_candidate = self.population.get_random_individual()
        second_candidate = self.population.get_random_individual()

        first_candidate_score = 0
        second_candidate_score = 0

        for i in range(self.GENOTYPE_QUANTITY):
            if first_candidate.genome[i] < second_candidate.genome[i]:
                first_candidate_score += 1
                continue
            if second_candidate.genome[i] < first_candidate.genome[i]:
                second_candidate_score += 1

        if first_candidate_score > second_candidate_score:
            return first_candidate

        return second_candidate

    def crossover(self):
        ''' Create a offspring population using the simulated binary crossover (SBX)
        and the binary tournament selection according to the crowded comparison operator..'''

        genomes_list = list()

        # Getting the quantity of individuals that are needed to create.
        # TODO: This value MUST BE even.
        amount_to_create = self.POPULATION_SIZE

        # "step = 2" because each iteration generates two children.
        for i in range(0, amount_to_create, 2):

            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()

            # Checking if crossover will or not be made.
            if random.random() > self.CROSSOVER_RATE:
                # When crossover isn't made, the children will be a clone of the parents.
                child1_genome = parent1.genome
                child2_genome = parent2.genome
            else:
                child1_genome, child2_genome = self.simulated_binary_crossover(parent1, parent2)

            genomes_list.append(child1_genome)
            genomes_list.append(child2_genome)

        # Creating the offspring population.
        offspring_population = self.new_population()

        # Adding the new children on that population.
        for child_genome in genomes_list:
            offspring_population.new_individual(self.mutation(child_genome))

        return offspring_population

    def usual_crossover(self):
        ''' Create a offspring population using the simulated binary crossover (SBX)
        and the usual binary tournament selection.'''

        # TODO: Call mutation function.

        genomes_list = list()

        # Getting the quantity of individuals that are needed to create.
        # TODO: This value MUST BE even.
        amount_to_create = self.POPULATION_SIZE

        # "step = 2" because each iteration generates two children.
        for i in range(0, amount_to_create, 2):

            parent1 = self.usual_tournament_selection()
            parent2 = self.usual_tournament_selection()

            child1_genome, child2_genome = self.simulated_binary_crossover(parent1, parent2)

            genomes_list.append(child1_genome)
            genomes_list.append(child2_genome)

        # Creating the offspring population.
        offspring_population = self.new_population()

        # Adding the new children on that.
        for child_genome in genomes_list:
            offspring_population.new_individual(child_genome)

        return offspring_population

    def simulated_binary_crossover(self, parent1, parent2):
        ''' Simulated binary crossover (SBX).'''

        # Distribution index. "nc" in NSGA-II paper.
        crossover_constant = self.CROSSOVER_CONSTANT

        child1_genome = list()
        child2_genome = list()

        for j in range(self.GENOTYPE_QUANTITY):

            # Each genotype has a 50% chance of changing its value.
            # TODO: This should be removed when dealing with one-dimensional solutions.
            if (random.random() > 0.5) and (self.GENOTYPE_QUANTITY != 1):
                # In this case, the children will get the value of the parents.
                child1_genome.append(parent1.genome[j])
                child2_genome.append(parent2.genome[j])
                continue

            # "y1" is the lowest value between parent1 and parent2. "y2" gets the other value.
            if (parent1.genome[j] < parent2.genome[j]):
                y1 = parent1.genome[j]
                y2 = parent2.genome[j]
            else:
                y1 = parent2.genome[j]
                y2 = parent1.genome[j]

            # EPS: precision error tolerance, its value is 1.0e-14 (global constant).
            eps = 0.000000000000010 #1.0e-14
            # If the value in parent1 is not the same of parent2.
            if abs(parent1.genome[j] - parent2.genome[j]) > eps:
                # Lower and upper limit of genotype of an individual.
                lower_bound = self.GENOME_MIN_VALUE
                upper_bound = self.GENOME_MAX_VALUE

                u = random.random()

                # Calculation of the first child.
                beta = 1 + (2 / (y2 - y1)) * min((y1 - lower_bound), (upper_bound - y2))
                alpha = 2 - pow(beta, -(crossover_constant + 1))
                if u <= (1/alpha):
                    beta_bar = pow(alpha * u, 1/(crossover_constant + 1))
                else:
                    beta_bar = pow(1/(2 - (alpha * u)), 1/(crossover_constant + 1))
                child1_genotype = 0.5 * ((y1 + y2) - beta_bar * (y2 - y1))

                # Calculation of the second child.
                beta = 1 + (2 / (y2 - y1)) * min((y1 - lower_bound), (upper_bound - y2))
                alpha = 2 - pow(beta, -(crossover_constant + 1))
                if u <= (1/alpha):
                    beta_bar = pow(alpha * u, 1/(crossover_constant + 1))
                else:
                    beta_bar = pow(1/(2 - (alpha * u)), 1/(crossover_constant + 1))
                child2_genotype = 0.5 * ((y1 + y2) + beta_bar * (y2 - y1))

                child1_genome.append(child1_genotype)
                child2_genome.append(child2_genotype)

            # The paper is not very clear about this, but i assume, in the equation of beta (not beta_bar),
            # y2 and y1, since they could not have been calculated yet, refer to the parents.
            # So, if both parents are equal at the specified variable, the divisor would be zero.
            # In this case, the children should have the same value as the parents. 
            else:
                child1_genome.append(parent1.genome[j])
                child2_genome.append(parent2.genome[j])

        return child1_genome, child2_genome

    def mutation(self, genome):
        '''Mutation method.'''

        debug = False

        random.seed()

        value = random.random()
        value = random.uniform(0, 1)
        # Checking if mutation will or not occur.
        if value > self.MUTATION_RATE:
            # When mutation doesn't occur, nothing happens.
            if debug: print("\n", value, "Mutation DOENS'T occur.")
            return genome

        if debug: print("\n", value, "Mutation occur.")
        if debug: print("Old genome:", genome)

        for i in range(len(genome)):
            # Mutate that genotype.
            if random.random() < self.GENOTYPE_MUTATION_PROBABILITY:

                value = (self.DISTURB_PERCENT * genome[i]) / 100.0

                # Will it add or decrease?
                if random.random() < 0.5:
                    value = -value

                if debug: print("Mutating the genotype", genome[i], " with: value =", value)

                genome[i] = genome[i] + value

                # Making sure that it doesn't escape the bounds.
                if genome[i] > self.GENOME_MAX_VALUE:
                    genome[i] = self.GENOME_MAX_VALUE
                elif genome[i] < self.GENOME_MIN_VALUE:
                    genome[i] = self.GENOME_MIN_VALUE

        if debug: print("New genome:", genome)

        return genome

    # Utils.
    def _show_fronts(self, fronts):
        '''Show all fronts.'''

        result = "FRONTS:\n"

        i = 0
        for front in fronts:
            i += 1
            result += "FRONT NUMBER " + str(i) + ":\n"

            j = 0
            for individual in front.individuals:
                j += 1
                result += (" [" + str(j) + "] " + str(individual) + "\n")

            result += "\n"

        print(result)

    def _show_population(self, population):
        '''Show all fronts.'''

        result = "POPULATION:\n"

        j = 0
        for individual in population.individuals:
            j += 1
            result += (" [" + str(j) + "] " + str(individual) + "\n")

        print(result)
