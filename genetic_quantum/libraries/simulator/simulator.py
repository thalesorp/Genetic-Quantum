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

'''File of Round Robin simulator class'''

class RoundRobinScheduler():
    '''Round Robin scheduling simulator'''

    def __init__(self, scenario, debug=None):
        if debug:
            self.debug = debug
        else:
            self.debug = False

        self.scenario = scenario
        self.processes = list()
        self.process_quantity = 0
        self.get_processes()

    def run(self, quantum):
        '''Simulate the round robin scheduling'''

        # Resulting metrics
        avg_turnaround_time = None
        avg_waiting_time = None
        context_switch = -1

        current_time = 0
        process_index = -1
        process_index = self.get_next_process_index(process_index)

        while process_index is not None:
            if self.debug == True: print("\ncurrent_time:", current_time)

            context_switch += 1

            remaining_time = quantum
            others_waiting_time = 0

            while self.processes[process_index].remaining_burst > 0 and remaining_time > 0:
                self.processes[process_index].consume_time_unit()
                current_time += 1
                remaining_time -= 1
                others_waiting_time += 1

            # Storing the current time as exit time
            self.processes[process_index].exit_time = current_time

            # Incrementing the waiting time of all other processes that are waiting right now
            self.increment_waiting_time(others_waiting_time, process_index)

            if self.debug == True: print(self.processes[process_index])

            process_index = self.get_next_process_index(process_index)

        if self.debug == True: print("\ncurrent_time:", current_time, "\nEnd of simulation.")

        total_turnaround_time = 0
        total_waiting_time = 0

        # Calculating the turnaround time of each process and the average
        # Also, calculating the average waiting time
        for process in self.processes:
            process.turnaround_time = process.exit_time - process.arrival_time
            total_turnaround_time += process.turnaround_time
            total_waiting_time += process.waiting_time
            if self.debug == True: print(process)

        avg_turnaround_time = total_turnaround_time / self.process_quantity
        avg_waiting_time = total_waiting_time / self.process_quantity

        # Reseting the processes for the possible next simulation
        self.reset_processes()

        if self.debug == True: print("avg_turnaround_time:", avg_turnaround_time)
        if self.debug == True: print("avg_waiting_time:", avg_waiting_time)
        if self.debug == True: print("context_switch:", context_switch)

        resulting_metrics = list([avg_turnaround_time, avg_waiting_time, context_switch])
        #resulting_metrics = list([avg_turnaround_time, avg_waiting_time])
        return resulting_metrics

    def get_processes(self):
        '''Get processes data from scenario file'''

        scenario_file = open(self.scenario, 'r')
        lines = scenario_file.readlines()

        for line in lines:
            # Ignoring commentaries and empty lines
            if line.find('#') != -1 or line == "\n":
                continue

            line = line.split(' ')

            if line[0] == 'P':
                # P [identifier] [arrival time] [burst time]
                process = Process(int(line[1]), int(line[2]), int(line[3]))
                self.processes.append(process)
                self.process_quantity += 1

    def reset_processes(self):
        ''' Reset the values inserted in each process of current scenario'''

        for process in self.processes:
            process.reset()

    def get_next_process_index(self, last_process_id):
        '''Return the next READY process in the processes list
        Return None when there's no avaliable READY process'''

        process_quantity = self.process_quantity

        for i in range(last_process_id+1, process_quantity):
            if self.processes[i].state == "R":
                return i

        for i in range(0, last_process_id+1):
            if self.processes[i].state == "R":
                return i

        return None

    def increment_waiting_time(self, time, current_process_index):
        '''Increment the "time" value to all READY process wainting time
        The process with id equals to "current_process_index" is ignored'''

        for process in self.processes:
            if process.identifier != self.processes[current_process_index].identifier:
                if process.state == "R":
                    process.waiting_time += time

    def worst_metrics(self):
        ''' Return the worst metrics. This is used as reference point in the
        hypervolume indicator calculation'''

        burst_summation = 0
        for process in self.processes:
            burst_summation += process.burst_time

        highest_burst = 0
        for process in self.processes:
            if process.burst_time > highest_burst:
                highest_burst = process.burst_time

        # [worst turaround time, worst waiting time, worst context switches]
        return [burst_summation, highest_burst, burst_summation]

class Process():
    '''Process class; used by Round Robin scheduling simulator'''

    def __init__(self, identifier=None, arrival_time=None, burst_time=None):
        self.identifier = identifier
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        self.remaining_burst = self.burst_time

        self.exit_time = 0

        self.turnaround_time = 0
        self.waiting_time = 0

        # READY or TERMINATED (R or T)
        self.state = "R"

    def consume_time_unit(self):
        '''Decreases one time unit from process remaining burst time
        When there's no more remaining burst, change state to TERMINATED'''

        self.remaining_burst -= 1
        if self.remaining_burst == 0:
            self.state = "T"

    def reset(self):
        '''Reset the process values so it can be used in the simulation'''

        self.remaining_burst = self.burst_time
        self.exit_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.state = "R"

    def __str__(self):
        result = ("id=" + str(self.identifier)
                + "  arrival=" + str(self.arrival_time)
                + "  burst=" + str(self.burst_time)
                + "  remaining_burst=" + str(self.remaining_burst)
                + "  turnaround_time=" + str(self.turnaround_time)
                + "  waiting_time=" + str(self.waiting_time)
                + "  state=" + str(self.state))
        return result
