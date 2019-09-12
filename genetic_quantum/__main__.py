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

'''Main.'''

from genetic_quantum import Genetic_quantum # pylint: disable=no-name-in-module

def main():
    genqua = Genetic_quantum()
    genqua.run()

if __name__ == '__main__':
    main()
