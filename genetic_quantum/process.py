#!/usr/bin/env python3

################################################################################
#                                                                              #
#  Genetic quantum:                                                            #
#    Finding a good quantum to Round-robin scheduling with NSGA-II             #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga                          #
#  Brazil, 2021                                                                #
#                                                                              #
#  Author: Thales Otávio                                                       #
#  Contact: @ThalesORP | ThalesORP@gmail.com                                   #
#                                                                              #
################################################################################

'''File of process class used by simulator class on simulator file.'''

class Process():
    '''Process class.'''

    def __init__(self, identifier=None, arrival_time=None, burst_time=None):
        self.identifier = identifier
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        self.remaining_burst = burst_time

        self.exit_time = 0

        self.turnaround_time = 0
        self.waiting_time = 0

        # READY or TERMINATED (R or T)
        self.state = "R"

    def consume_time_unit(self):
        '''Decreases one time unit from process remaining burst time.
        When there's no more remaining burst, change state to TERMINATED.'''

        self.remaining_burst -= 1
        if self.remaining_burst == 0:
            self.state = "T"

    def __str__(self):
        result = ("id=" + str(self.identifier)
                + "  arrival=" + str(self.arrival_time)
                + "  burst=" + str(self.burst_time)
                + "  remaining_burst=" + str(self.remaining_burst)
                + "  turnaround_time=" + str(self.turnaround_time)
                + "  waiting_time=" + str(self.waiting_time)
                + "  state=" + str(self.state))
        return result
