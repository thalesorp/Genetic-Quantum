#!/usr/bin/env bash

# Usage:
#./factorial-experiment.sh 2 2 2 2 10 01 > experiment-01-results.txt
#./factorial-experiment.sh 2 2 2 1 10 02 > experiment-02-results.txt
#./factorial-experiment.sh 2 2 1 2 10 03 > experiment-03-results.txt
#./factorial-experiment.sh 2 2 1 1 10 04 > experiment-04-results.txt

#./factorial-experiment.sh 2 1 2 2 10 05 > experiment-05-results.txt
#./factorial-experiment.sh 2 1 2 1 10 06 > experiment-06-results.txt
#./factorial-experiment.sh 2 1 1 2 10 07 > experiment-07-results.txt
#./factorial-experiment.sh 2 1 1 1 10 08 > experiment-08-results.txt

#./factorial-experiment.sh 1 2 2 2 10 09 > experiment-09-results.txt
#./factorial-experiment.sh 1 2 2 1 10 10 > experiment-10-results.txt
#./factorial-experiment.sh 1 2 1 2 10 11 > experiment-11-results.txt
#./factorial-experiment.sh 1 2 1 1 10 12 > experiment-12-results.txt

#./factorial-experiment.sh 1 1 2 2 10 13 > experiment-13-results.txt
#./factorial-experiment.sh 1 1 2 1 10 14 > experiment-14-results.txt
#./factorial-experiment.sh 1 1 1 2 10 15 > experiment-15-results.txt
#./factorial-experiment.sh 1 1 1 1 10 16 > experiment-16-results.txt


SCENARIO="resources/scenarios/test-dataset/Dataset-2_20-80/Case-3_50-processes.txt"
MIN_QUANTUM="1"
MAX_QUANTUM="25"

GENERATIONS_INDEX=$1
POPULATION_SIZE_INDEX=$2
CROSSOVER_CONSTANT_INDEX=$3
CROSSOVER_RATE_INDEX=$4
EXECUTIONS=$5
CONFIG_N=$6

(( GENERATIONS_INDEX-- ))
(( POPULATION_SIZE_INDEX-- ))
(( CROSSOVER_CONSTANT_INDEX-- ))
(( CROSSOVER_RATE_INDEX-- ))

GENERATIONS=(8 20)
POPULATION_SIZE=(150 200)
CROSSOVER_CONSTANT=(1 3)
CROSSOVER_RATE=(0.85 0.95)

GENERATIONS=${GENERATIONS[$GENERATIONS_INDEX]}
POPULATION_SIZE=${POPULATION_SIZE[$POPULATION_SIZE_INDEX]}
CROSSOVER_CONSTANT=${CROSSOVER_CONSTANT[$CROSSOVER_CONSTANT_INDEX]}
CROSSOVER_RATE=${CROSSOVER_RATE[$CROSSOVER_RATE_INDEX]}

FACTORIAL_EXPERIMENT_FOLDER="factorial-experiment"
mkdir -p $FACTORIAL_EXPERIMENT_FOLDER

FILES_PREFIX="Config-"$CONFIG_N"_"$GENERATIONS"-"$POPULATION_SIZE"-"$CROSSOVER_CONSTANT"-"$CROSSOVER_RATE

FINAL_RESULTS_OUTPUT_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-"$EXECUTIONS"-executions_final-results.txt"

echo "# Factorial experiment"
echo "#"
echo "# A: Generations="$GENERATIONS
echo "# B: Population_size="$POPULATION_SIZE
echo "# C: Crossover_constant="$CROSSOVER_CONSTANT
echo "# D: Crossover_rate="$CROSSOVER_RATE
echo "# Executions="$EXECUTIONS
echo "#"
echo "#"

#################################################### Genetic Quantum ###################################################

SECONDS=0

for i in $(seq $EXECUTIONS)
do
    echo "# `date +"[%Y-%m-%d %H:%M:%S]"` Running Genetic Quantum. Execution $i of $EXECUTIONS..."
    EXECUTION_RESULT_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-$i-of-$EXECUTIONS.txt"
    echo "# [NAME] [QUANTUM] [TURNAROUND TIME] [WAITING TIME] [CONTEXT SWITCHES] [NONDOMINATED RANK] [CROWDING DISTANCE]" > $EXECUTION_RESULT_FILE
    ./genetic_quantum.py $SCENARIO $GENERATIONS $POPULATION_SIZE $MIN_QUANTUM $MAX_QUANTUM $CROSSOVER_CONSTANT $CROSSOVER_RATE >> $EXECUTION_RESULT_FILE
done

RUNTIME=$SECONDS

####################################################### Statistics #####################################################

# Normalizing values: Fiding the highest values of each metric
MAX_TURNAROUND=$(cat $FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-*-of-$EXECUTIONS.txt | awk '!/#/{print }' | awk '{print $3};' | ./statistics.sh \
                | tee $FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-"$EXECUTIONS"-executions_statistics-turaround-time.txt | egrep "Max:" | sed 's/^[A-Za-z]*:\s//')

MAX_WAITING=$(cat $FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-*-of-$EXECUTIONS.txt | awk '!/#/{print }' | awk '{print $4};' | ./statistics.sh \
                | tee $FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-"$EXECUTIONS"-executions_statistics-waiting-time.txt | egrep "Max:" | sed 's/^[A-Za-z]*:\s//')

MAX_CONTEXT_SWITCHES=$(cat $FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-*-of-$EXECUTIONS.txt | awk '!/#/{print }' | awk '{print $5};' | ./statistics.sh \
                | tee $FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-"$EXECUTIONS"-executions_statistics-context-switches.txt | egrep "Max:" | sed 's/^[A-Za-z]*:\s//')

# Normalizing values: dividing all metrics in all files by the highest value previously found
for i in $(seq $EXECUTIONS)
do
    NORMALIZED_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-$i-of-"$EXECUTIONS"_normalized.txt"
    EXECUTION_RESULT_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-$i-of-$EXECUTIONS.txt"
    cat $EXECUTION_RESULT_FILE \
    | awk -v maxT=$MAX_TURNAROUND -v maxW=$MAX_WAITING -v maxC=$MAX_CONTEXT_SWITCHES '{ if($1 != "#" && $1 != "") { $3 = ( (float) $3 / maxT) ; $4 = ( (float) $4 / maxW) ; $5 = ( (float) $5 / maxC) } ; print $0; }' \
    > $NORMALIZED_FILE
done

# Calculating the hypervolume indicator
HYPERVOLUMES_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-"$EXECUTIONS"-executions_hypervolumes.txt"
echo "# [HYPERVOLUME]" > $HYPERVOLUMES_FILE

for i in $(seq $EXECUTIONS)
do
    # Creating the input files for the hypervolume
    NORMALIZED_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-$i-of-"$EXECUTIONS"_normalized.txt"
    HYPERVOLUME_FRONT_FILE="$FACTORIAL_EXPERIMENT_FOLDER/"$FILES_PREFIX"_results-of-execution-$i-of-"$EXECUTIONS"_normalized_hypervolume-input.txt"

    # TODO: Colocar ponto de referência como variável! ################################################################# <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- <- !!!
    echo "{\"objective\":[1, 1, 1]}" > $HYPERVOLUME_FRONT_FILE
    echo -n "[" >> $HYPERVOLUME_FRONT_FILE

    cat $NORMALIZED_FILE | awk '{if ($1 != "#" && $1 != "") {print "{\"objective\":["$3", "$4", "$5"]}, "}}' > ${HYPERVOLUME_FRONT_FILE}.tmp
    echo "]" >> ${HYPERVOLUME_FRONT_FILE}.tmp
    cat ${HYPERVOLUME_FRONT_FILE}.tmp | tr "\n" " " | sed 's/\]}, *\]/\]}/' | sed 's/  / /g' >> $HYPERVOLUME_FRONT_FILE

    echo "]" >> $HYPERVOLUME_FRONT_FILE

    rm ${HYPERVOLUME_FRONT_FILE}.tmp

    HYPERVOLUME=$(python3 -W ignore libraries/hypervolume/hv.py -q -r '[1, 1, 1]' < $HYPERVOLUME_FRONT_FILE)
    echo $HYPERVOLUME | sed 's/{"score": //g' | sed 's/}//g' >> $HYPERVOLUMES_FILE
done

HYPERVOLUME_MEAN=$(cat $HYPERVOLUMES_FILE | awk '!/#/{print }' | awk 'BEGIN{sum = 0.0; }{ sum += $1; }END{ print sum/NR;  }')

echo "#"
echo "#"
echo "# [HYPERVOLUME MEAN] [TOTAL RUNTIME]"
printf $HYPERVOLUME_MEAN"\t"$RUNTIME"\n"
