#!/bin/bash

COMPUTING_TIMES=10

LAST_ROW=$(($COMPUTING_TIMES + 2))

QUANTUM=5

SCENARIO_FILES=(../../resources/scenarios/probabilistic/probabilistic_scenario_1.txt ../../resources/scenarios/probabilistic/probabilistic_scenario_2.txt ../../resources/scenarios/probabilistic/probabilistic_scenario_3.txt ../../resources/scenarios/probabilistic/probabilistic_scenario_4.txt ../../resources/scenarios/probabilistic/probabilistic_scenario_5.txt ../../resources/scenarios/probabilistic/probabilistic_scenario_6.txt)
#SCENARIO_FILES=$(for i in $(seq 6) ; do echo -n "../../resources/scenarios/probabilistic/probabilistic_scenario_1$i.txt " ; done)

RESULTS=(probabilistic_scenario_1-result.csv probabilistic_scenario_2-result.csv probabilistic_scenario_3-result.csv probabilistic_scenario_4-result.csv probabilistic_scenario_5-result.csv probabilistic_scenario_6-result.csv)
#RESULTS=$(for i in $(seq 6) ; do echo -n "probabilistic_scenario_$i-result.csv " ; done)

OUTPUT_DIR=Output

# Formatando a saída do comando GNU "time".
TIMEFORMAT='%3R'

# Pasta de destino dos arquivos que serão montados abaixo.
mkdir $OUTPUT_DIR

for i in $(seq 1 ${#SCENARIO_FILES[@]}) ; do

    for j in $(seq 1 $COMPUTING_TIMES) ; do
        echo -e $j >> ${RESULTS[i-1]}
        #{ time ./sim_pro/SimPro.exe RR $QUANTUM ${SCENARIO_FILES[i-1]} P ; } 2>> ${RESULTS[i-1]}
        { time python2 simpro/SimPro.py RR $QUANTUM ${SCENARIO_FILES[i-1]} P ; } 2>> ${RESULTS[i-1]}
    done

    # Formatando o arquivo para ".csv":
    # Substitui as vírgulas por pontos.
    sed -i 's/,/./g' ${RESULTS[i-1]}
    # Remove quebra de linhas e separa os valores por vírgula.
    sed -i 'N;s/\n/,/' ${RESULTS[i-1]}
    # Inserindo o "abre asplas duplas".
    sed -i 's/,/,"/g' ${RESULTS[i-1]}
    # Inserindo o "fecha aspas duplas".
    sed -i 's/$/"/' ${RESULTS[i-1]}
    # Substituindo de volta pos pontos por vírgulas.
    sed -i 's/\./,/g' ${RESULTS[i-1]}
    # Insere o cabeçalho.
    sed -i '1s/^/EXECUTION,TIME\n/' ${RESULTS[i-1]}
    # Inserindo quebra de linha na tabela.
    sed -i -e "\$a," ${RESULTS[i-1]}
    # Inserindo o cálculo da média.
    sed -i -e "\$aMédia =,=MÉDIA(B2:B$LAST_ROW)" ${RESULTS[i-1]}
    # Inserindo o cálculo da mediana.
    sed -i -e "\$aMediana =,=MED(B2:B$LAST_ROW)" ${RESULTS[i-1]}

    mv ${RESULTS[i-1]} $OUTPUT_DIR/
done

# Formatando a saída do comando GNU "time" para o padrão.
TIMEFORMAT=$'\nreal\t%3lR\nuser\t%3lU\nsys\t%3lS'

exit 0
