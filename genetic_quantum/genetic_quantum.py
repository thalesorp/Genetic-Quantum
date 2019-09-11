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

'''Class'''

from lib.nsga2.nsga2 import NSGA2 # pylint: disable=import-error

class Genetic_quantum(NSGA2):

    def __init__(self):
        self.foo = None

    def run(self):
        '''Method responsible for calling the NSGA-II.'''
        my_nsga2 = NSGA2()
        my_nsga2.run()
