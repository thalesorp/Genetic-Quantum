#!/usr/bin/env python3
#
# Genetic quantum
# An adaptive process scheduler based on Round-robin and optmized with NSGA-II
#
# Instituto Federal de Minas Gerais - Campus Formiga, Brazil
#
# Version 1.0
# (c) 2021 Thales Pinto <ThalesORP@gmail.com> under the GPL
#          http://www.gnu.org/copyleft/gpl.html
#

'''Root file of this project'''

from libraries.nsga2.nsga2 import NSGA2
from libraries.nsga2.individual import Individual
from libraries.simulator.simulator import RoundRobinScheduler

from math import sqrt, sin, pi

#import matplotlib.pyplot as plt
#import numpy as np
#import random
#import imageio
#import os
#import statistics

import sys
import datetime
import time
from pathlib import Path

class GeneticQantum(NSGA2):
    '''Main class of this project'''

    # "ZDT1", "ZDT2", "ZDT3" or "GQ"
    TEST_PROBLEM = "GQ"

    def __init__(self, scenario, generations, population_size, genome_min_value, genome_max_value, crossover_constant, crossover_rate):
        # Calling the parent constructor
        super().__init__(generations, population_size, genome_min_value, genome_max_value, crossover_constant, crossover_rate)

        self.PLOTS_FOLDER = "resources/" + self.TEST_PROBLEM + "-plots/"
        self.FILE_PREFIX = "Img_"
        self.FILE_FORMAT = ".png"

        self.color_counter = -1
        self.colors = ['bo', 'go', 'ro', 'co', 'mo', 'yo', 'ko']

        self.SCENARIO = scenario

        self.round_robin = RoundRobinScheduler(self.SCENARIO)

        #self.nsga2_results_folder = "resources/nsga2-results/"
        #Path(self.nsga2_results_folder).mkdir(parents=True, exist_ok=True)

        self.hypervolume_lib_folder = "libraries/hypervolume/"
        Path(self.hypervolume_lib_folder).mkdir(parents=True, exist_ok=True)

        self.front_file_name = "best_front.txt"

    def run(self):
        start_time = time.time()
        best_front = super().run()
        runtime = time.time() - start_time

        #sys.stderr.write("debug!")

        # [NAME] [QUANTUM] [NORMALIZED TURNAROUND TIME] [NORMALIZED WAITING TIME] [NORMALIZED CONTEXT SWITCHES] [NONDOMINATED RANK] [CROWDING DISTANCE] [TURNAROUND TIME] [WAITING TIME] [CONTEXT SWITCHES]
        output = ""
        for individual in best_front.individuals:
            output += str(individual.name) + " "
            output += str(individual.genome[0]) + " "
            output += str(individual.solutions[0]) + " "
            output += str(individual.solutions[1]) + " "
            output += str(individual.solutions[2]) + " "
            output += str(individual.non_normalized_solutions[0]) + " "
            output += str(individual.non_normalized_solutions[1]) + " "
            output += str(individual.non_normalized_solutions[2]) + "\n"
            #output += str(individual.rank) + " "
            #output += str(individual.crowding_distance) + "\n"

        print(output)

    # NSGA-II
    def evaluate(self, population):
        '''How the individuals are evaluated'''

        if self.TEST_PROBLEM.upper() == "GQ":
            for individual in population.individuals:
                # Evaluating only the individuals that doesn't have been evaluated before
                if not individual.solutions:
                    quantum = individual.genome[0]
                    solutions = self.round_robin.run(quantum)
                    individual.solutions = solutions

        if self.TEST_PROBLEM.upper() == "ZDT1":
            for individual in population.individuals:
                # Evaluating only the individuals that doesn't have been evaluated before
                if not individual.solutions:
                    individual.solutions = self.zdt1(individual.genome)

        if self.TEST_PROBLEM.upper() == "ZDT2":
            for individual in population.individuals:
                # Evaluating only the individuals that doesn't have been evaluated before
                if not individual.solutions:
                    individual.solutions = self.zdt2(individual.genome)

        if self.TEST_PROBLEM.upper() == "ZDT3":
            for individual in population.individuals:
                # Evaluating only the individuals that doesn't have been evaluated before
                if not individual.solutions:
                    individual.solutions = self.zdt3(individual.genome)

    # Objective function
    def zdt1(self, x):
        n = len(x)
        f1 = x[0]
        g = 1 + 9/(n-1) * sum(x[1:])
        h = 1 - sqrt(f1/g)
        f2 = g * h
        return [f1, f2]

    def zdt2(self, x):
        n = len(x)
        f1 = x[0]
        g = 1 + 9/(n-1) * sum(x[1:])
        h = 1 - ((f1/g)**2)
        f2 = g * h
        return [f1, f2]

    def zdt3(self, x):
        n = len(x)
        f1 = x[0]
        g = 1 + 9/(n-1) * sum(x[1:])
        h = 1 - sqrt(f1/g) - ((f1/g) * sin(10 * pi * f1))
        f2 = g * h
        return [f1, f2]

    # NSGA-II: fitness function
    def evaluate(self, population):
        '''Call the round robin scheduling simulator to get the solutions for each quantum proposed by the NSGA-II algorithm'''

        max_turnaround_time = 0
        max_waiting_time = 0
        max_context_switches = 0

        # Calling the simulator and getting the solutions
        for individual in population.individuals:
            # Evaluating only the individuals that doesn't have been evaluated before
            if not individual.solutions:
                quantum = individual.genome[0]
                # Saving the non normalized solutions
                individual.non_normalized_solutions = self.round_robin.run(quantum)

        # Updating the max values of each solution
        for individual in population.individuals:
            #solutions = [avg_turnaround_time, avg_waiting_time, context_switch]
            if individual.non_normalized_solutions[0] > max_turnaround_time:
                max_turnaround_time = individual.non_normalized_solutions[0]

            if individual.non_normalized_solutions[1] > max_waiting_time:
                max_waiting_time = individual.non_normalized_solutions[1]

            if individual.non_normalized_solutions[2] > max_context_switches:
                max_context_switches = individual.non_normalized_solutions[2]

        # Normalizing the values of each solution and putting them into individuals.solutions list
        for individual in population.individuals:
            individual.solutions.append(individual.non_normalized_solutions[0] / max_turnaround_time)
            individual.solutions.append(individual.non_normalized_solutions[1] / max_waiting_time)
            individual.solutions.append(individual.non_normalized_solutions[2] / max_context_switches)

    # Hypervolume indicator
    def create_front_file(self, best_front, reference_point):
        '''Putting the best front into the format of hypervolume calculation input'''

        with open(self.hypervolume_lib_folder + self.front_file_name, "w") as file_:
            file_.write("{\"objective\":" + str([1] * len(reference_point)) + "}\n")

            objectives = "["
            for individual in best_front.individuals:
                objectives += "{\"objective\":" + str(individual.solutions) + "}, "
            objectives = objectives[:-2] + "]\n"

            file_.write(objectives)

    # NSGA-II results file
    def _generate_results(self, front):
        '''Create a file and insert the resulting data'''

        now = datetime.datetime.now()
        results_file_name = str(self.nsga2_results_folder + now.strftime('%Y-%m-%d_%H-%M-%S') + "_nsga2-results" + '.txt')

        output = "# [NAME] [QUANTUM] [TURNAROUND TIME] [WAITING TIME] [CONTEXT SWITCHES] [NONDOMINATED RANK] [CROWDING DISTANCE]\n"
        for individual in front.individuals:
            output += str(individual.name) + " "
            output += str(individual.genome[0]) + " "
            output += str(individual.solutions[0]) + " "
            output += str(individual.solutions[1]) + " "
            output += str(individual.solutions[2]) + " "
            output += str(individual.rank) + " "
            output += str(individual.crowding_distance) + "\n"

        with open(results_file_name, "w") as file_:
            file_.write(output)

scenario = sys.argv[1]
generations = int(sys.argv[2])
population_size = int(sys.argv[3])
genome_min_value = int(sys.argv[4])
genome_max_value = int(sys.argv[5])
crossover_constant = int(sys.argv[6])
crossover_rate = float(sys.argv[7])

GeneticQantum(scenario, generations, population_size, genome_min_value, genome_max_value, crossover_constant, crossover_rate).run()
