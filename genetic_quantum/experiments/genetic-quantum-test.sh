#!/usr/bin/env bash

SCENARIO="resources/scenarios/new-test-dataset/Case-50-processes_zero-arrival-time.txt"
#SCENARIO="resources/scenarios/new-test-dataset/Case-50-processes_non-zero-arrival-time.txt"

GENERATIONS=20
POPULATION_SIZE=150

MIN_QUANTUM="1"
MAX_QUANTUM=$(awk '!/#/{print $4}' $SCENARIO | ./statistics.sh | egrep "Max:" | sed 's/^[A-Za-z]*:\s//')
MAX_QUANTUM=${MAX_QUANTUM%???}

CROSSOVER_CONSTANT=3
CROSSOVER_RATE=0.95

echo "# Genetic Quantum test"
echo "# "
echo "# Generations: "$GENERATIONS
echo "# Population size: "$POPULATION_SIZE
echo "# Minimum quantum: "$MIN_QUANTUM
echo "# Maximum quantum: "$MAX_QUANTUM
echo "# Crossover constant: "$CROSSOVER_CONSTANT
echo "# Crossover rate: "$CROSSOVER_RATE
echo "# Scenario:"$SCENARIO
echo "# "
echo "# "

./genetic_quantum.py $SCENARIO $GENERATIONS $POPULATION_SIZE $MIN_QUANTUM $MAX_QUANTUM $CROSSOVER_CONSTANT $CROSSOVER_RATE
