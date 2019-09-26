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

'''File of individual class.'''

class Individual():
    '''Individuals calss of the population in NSGA-II.'''

    def __init__(self, chromosome):

        # The actual value of current individual.
        self.chromosome = chromosome

        # List of solutions. Each position is one objective function.
        self.solutions = list()

        # Quantity of individuals that dominates this individual.
        self.domination_count = 0

        # List of individuals that are dominated by this individual.
        self.dominated_by = list()

        self.crowding_distance = 0

    def __str__(self):
        result = "Individual (quantum=" + str(self.chromosome) + ") Solutions -> "
        for i in range(len(self.solutions)-1):
            result += str(self.solutions[i]) + ", "
        result += str(self.solutions[i])
        return result

    def __simple_str__(self):
        if not self.solutions:
            return "()"

        result = "("

        for i in range(len(self.solutions)-1):
            result += str(self.solutions[i]) + ", "
        result += str(self.solutions[i]) + ")"

        return result

    def dominates(self, individual):
        '''Function that tells if the actual individual dominates another.

        A(x1, y1) dominates B(x2, y2) when:
            (x1 <= x2 and y1 <= y2) and (x1 < x2 or y1 < y2)

        A(x1, y1, z1) dominates B(x2, y2, z2) when:
            [ (x1 <= x2) and (y1 <= y2) and (z1 <= z2) ] and [ (x1 < x2) or (y1 < y2) or (z1 < z2) ]
            [ first_half ] and [ second_half ]'''

        first_half = None
        second_half = None

        i = 0
        for solution in self.solutions:
            first_half = first_half and bool(solution <= individual.solutions[i])
            second_half = second_half or bool(solution < individual.solutions[i])
            i += 1
        return first_half and second_half

    def evaluate(self):
        ''' How individuals are evaluated.'''
