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

from libraries.nsga2.nsga2 import NSGA2 # pylint: disable=import-error

class Genetic_quantum(NSGA2):

    def __init__(self):
        # Calling the parent constructor.
        NSGA2.__init__(self)

    def run(self):
        '''Method responsible for calling the NSGA-II.'''
        super(Genetic_quantum, self).run()
