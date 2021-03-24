#!/usr/bin/env bash

MIN_QUANTUM="1"

GENERATIONS=20
POPULATION_SIZE=150
CROSSOVER_CONSTANT=3
CROSSOVER_RATE=0.95

EXECUTIONS=100

ROOT="final-experiment"
mkdir -p $ROOT

FILE_PREFIX="final-experiment"

echo "# Final experiment"
echo "# "
echo "# Generations: "$GENERATIONS
echo "# Population size: "$POPULATION_SIZE
echo "# Crossover constant: "$CROSSOVER_CONSTANT
echo "# Crossover rate: "$CROSSOVER_RATE
echo "# Executions: "$EXECUTIONS
echo "# "
echo "# "

declare -a SCENARIOS_PATH=("resources/scenarios/dataset-1/case-1.txt"
                           "resources/scenarios/dataset-1/case-2.txt"
                           "resources/scenarios/dataset-1/case-3.txt"
                           "resources/scenarios/dataset-1/case-4.txt"
                           "resources/scenarios/dataset-1/case-5.txt"
                           "resources/scenarios/dataset-1/case-6.txt"

                           "resources/scenarios/dataset-2/case-1.txt"
                           "resources/scenarios/dataset-2/case-2.txt"
                           "resources/scenarios/dataset-2/case-3.txt"
                           "resources/scenarios/dataset-2/case-4.txt"

                           "resources/scenarios/dataset-3/case-1_28-80_50-processes.txt"
                           "resources/scenarios/dataset-3/case-2_50-processes_zero-arrival-time.txt"
                           "resources/scenarios/dataset-3/case-3_50-processes_non-zero-arrival-time.txt")

declare -a SCENARIOS_NAME=("dataset-1_case-1"
                           "dataset-1_case-2"
                           "dataset-1_case-3"
                           "dataset-1_case-4"
                           "dataset-1_case-5"
                           "dataset-1_case-6"

                           "dataset-2_case-1"
                           "dataset-2_case-2"
                           "dataset-2_case-3"
                           "dataset-2_case-4"

                           "dataset-3_case-1_28-80_50-processes"
                           "dataset-3_case-2_50-processes_zero-arrival-time"
                           "dataset-3_case-3_50-processes_non-zero-arrival-time")

SECONDS=0

for i in `seq 0 $(( ${#SCENARIOS_NAME[@]} - 1 ))`
do
    SCENARIO_PATH=${SCENARIOS_PATH[$i]}
    SCENARIO=${SCENARIOS_NAME[$i]}
    mkdir -p $ROOT/$SCENARIO

    MAX_QUANTUM=$(awk '!/#/{print $4}' $SCENARIO_PATH | ./statistics.sh | egrep "Max:" | sed 's/^[A-Za-z]*:\s//')
    MAX_QUANTUM=${MAX_QUANTUM%???}

    echo "# Scenario: "\"$SCENARIO\"

    for j in $(seq $EXECUTIONS)
    do
        PREFIX="$ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-$j-of-"$EXECUTIONS
        EXECUTION_OUTPUT_FILE=$PREFIX"_results.txt"

        echo "# `date +"[%Y-%m-%d %H:%M:%S]"` Running Genetic Quantum. Execution $j of $EXECUTIONS..."

        # File header
        FILE_HEADER="# Final experiment\n"
        FILE_HEADER+="# Execution $j of $EXECUTIONS\n"
        FILE_HEADER+="# \n"
        FILE_HEADER+="# Generations: "$GENERATIONS"\n"
        FILE_HEADER+="# Population size: "$POPULATION_SIZE"\n"
        FILE_HEADER+="# Minimum quantum: "$MIN_QUANTUM"\n"
        FILE_HEADER+="# Maximum quantum: "$MAX_QUANTUM"\n"
        FILE_HEADER+="# Crossover constant: "$CROSSOVER_CONSTANT"\n"
        FILE_HEADER+="# Crossover rate: "$CROSSOVER_RATE"\n"
        FILE_HEADER+="# Scenario: "\"$SCENARIO\""\n"
        FILE_HEADER+="# \n"
        FILE_HEADER+="# \n"
        #FILE_HEADER+="# [NAME] [QUANTUM] [NORMALIZED TURNAROUND TIME] [NORMALIZED WAITING TIME] [NORMALIZED CONTEXT SWITCHES] [TURNAROUND TIME] [WAITING TIME] [CONTEXT SWITCHES] [NONDOMINATED RANK] [CROWDING DISTANCE]"
        FILE_HEADER+="# [NAME] [QUANTUM] [NORMALIZED TURNAROUND TIME] [NORMALIZED WAITING TIME] [NORMALIZED CONTEXT SWITCHES] [TURNAROUND TIME] [WAITING TIME] [CONTEXT SWITCHES]"
        echo -e $FILE_HEADER > $EXECUTION_OUTPUT_FILE

        # Execution
        ./genetic_quantum.py $SCENARIO_PATH $GENERATIONS $POPULATION_SIZE $MIN_QUANTUM $MAX_QUANTUM $CROSSOVER_CONSTANT $CROSSOVER_RATE >> $EXECUTION_OUTPUT_FILE
    done


    # Statistics
    TURNAROUND_STATISTICS_FILE="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_turnaround-time"
    WAITING_STATISTICS_FILE="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_waiting-time"
    CONTEXT_SWITCHES_STATISTICS_FILE="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_context-switches"

    #cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS".txt | awk '!/#/{print }' | awk '{print $3};' | ./statistics.sh | egrep "Max:" | sed 's/^[A-Za-z]*:\s//'
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print }' | awk '{print $3};' | ./statistics.sh > ${TURNAROUND_STATISTICS_FILE}-norm.txt
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print }' | awk '{print $4};' | ./statistics.sh > ${WAITING_STATISTICS_FILE}-norm.txt
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print }' | awk '{print $5};' | ./statistics.sh > ${CONTEXT_SWITCHES_STATISTICS_FILE}-norm.txt


    QUANTUM_COLUMN="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_quantum"
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print $2}' > $QUANTUM_COLUMN
    echo -n "# " ; ./plot-summary.sh $QUANTUM_COLUMN

    TURNAROUND_TIME_COLUMN="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_turnaround-time"
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print $6}' > $TURNAROUND_TIME_COLUMN
    echo -n "# " ; ./plot-summary.sh $TURNAROUND_TIME_COLUMN

    WAITING_TIME_COLUMN="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_waiting-time"
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print $7}' > $WAITING_TIME_COLUMN
    echo -n "# " ; ./plot-summary.sh $WAITING_TIME_COLUMN

    CONTEXT_SWTICHES_COLUMN="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"_statistics_context-switches"
    cat $ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-*-of-"$EXECUTIONS"_results.txt | awk '!/#/{print $8}' > $CONTEXT_SWTICHES_COLUMN
    echo -n "# " ; ./plot-summary.sh $CONTEXT_SWTICHES_COLUMN

    # Delete temporary file
    rm $QUANTUM_COLUMN
    rm $TURNAROUND_TIME_COLUMN
    rm $WAITING_TIME_COLUMN
    rm $CONTEXT_SWTICHES_COLUMN

    echo "# "
    echo "# "

done

RUNTIME=$SECONDS

# Hypervolume
for i in `seq 0 $(( ${#SCENARIOS_NAME[@]} - 1 ))`
do
    SCENARIO=${SCENARIOS_NAME[$i]}

    # Calculating the hypervolume indicator
    HYPERVOLUMES_FILE="$ROOT/$SCENARIO/"$FILE_PREFIX"_Executions-"$EXECUTIONS"-hypervolumes.txt"
    echo "# [HYPERVOLUME]" > $HYPERVOLUMES_FILE

    for j in $(seq $EXECUTIONS)
    do
        PREFIX="$ROOT/$SCENARIO/"$FILE_PREFIX"_Execution-$j-of-"$EXECUTIONS

        # Creating the input files for the hypervolume
        EXECUTION_OUTPUT_FILE=$PREFIX"_results.txt"

        HYPERVOLUME_FRONT_FILE=$PREFIX"_results_hypervolume-input.txt"

        echo "{\"objective\":[1, 1, 1]}" > $HYPERVOLUME_FRONT_FILE
        echo -n "[" >> $HYPERVOLUME_FRONT_FILE

        cat $EXECUTION_OUTPUT_FILE | awk '{if ($1 != "#" && $1 != "") {print "{\"objective\":["$3", "$4", "$5"]}, "}}' > ${HYPERVOLUME_FRONT_FILE}.tmp
        echo "]" >> ${HYPERVOLUME_FRONT_FILE}.tmp
        cat ${HYPERVOLUME_FRONT_FILE}.tmp | tr "\n" " " | sed 's/\]}, *\]/\]}/' | sed 's/  / /g' >> $HYPERVOLUME_FRONT_FILE

        echo "]" >> $HYPERVOLUME_FRONT_FILE

        rm ${HYPERVOLUME_FRONT_FILE}.tmp

        HYPERVOLUME=$(python3 -W ignore libraries/hypervolume/hv.py -q -r '[1, 1, 1]' < $HYPERVOLUME_FRONT_FILE)
        echo $HYPERVOLUME | sed 's/{"score": //g' | sed 's/}//g' >> $HYPERVOLUMES_FILE
    done

    HYPERVOLUME_MEAN=$(cat $HYPERVOLUMES_FILE | awk '!/#/{print }' | awk 'BEGIN{sum = 0.0; }{ sum += $1; }END{ print sum/NR;  }')

done

echo "#"
echo "#"
echo "# [HYPERVOLUME MEAN] [TOTAL RUNTIME]"
printf $HYPERVOLUME_MEAN"\t"$RUNTIME"\n"

#if false
#then
    # COMMENT
#fi
