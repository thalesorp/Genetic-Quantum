#!/usr/bin/env python3

################################################################################
#                                                                              #
#  SimPro:                                                                     #
#    Simulador de escalonamento de processos                                   #
#                                                                              #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019                    #
#                                                                              #
#  Orientador: Diego Mello Silva                                               #
#  Aluno: Danilo da Silva Alves                                                #
#                                                                              #
################################################################################

''' Module docstring.'''

class Cenario():
    ''' Class docstring.'''

    def __init__(self):
        self.tempoSimulacao = 0.0
        self.nCPUs = 0
        self.nDispositivos = 0

        self.tempoChegadaProcesso = 0
        self.tempoEncProcesso = list()
        self.nIObursts = list()
        self.duracaoCPUburst = list()
        self.duracaoIOburst = list()
        self.prioridade = list()

        self.listaDeProcessos = list()

    def carregaCenario(self, file_name, modelo):
        ''' Method docstring.'''

        cenario = open(file_name, 'r')
        texto = cenario.readlines()

        if modelo == 'D':
            for linha in texto:
                if linha.find('#') != -1:
                    # Ignorando comentários.
                    continue

                linha = linha.split(' ')

                # Dados de processo.
                if linha[0] == 'P':
                    # [id, chegada, CPUburst, prioridade]
                    p = [int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4])]
                    self.listaDeProcessos.append(p)

        elif modelo == 'P':
            for linha in texto:
                if linha.find('#') != -1:
                    # Ignorando comentários.
                    continue

                linha = linha.split(' ')

                # Dados da simulação.
                if linha[0] == 'S':
                    if linha[1] == 'TS':
                        self.tempoSimulacao = int(linha[2])

                # Dados de processos.
                elif linha[0] == 'P':
                    if linha[1] == 'CH':
                        self.tempoChegadaProcesso = float(linha[2])
                    elif linha[1] == 'PR':
                        self.prioridade.append(float(linha[2]))
                        self.prioridade.append(float(linha[3]))
                        self.prioridade.append(float(linha[4]))
                    elif linha[1] == 'EN':
                        self.tempoEncProcesso.append(float(linha[2]))
                        self.tempoEncProcesso.append(float(linha[3]))
                        self.tempoEncProcesso.append(float(linha[4]))
                    elif linha[1] == 'NI':
                        self.nIObursts.append(float(linha[2]))
                        self.nIObursts.append(float(linha[3]))
                        self.nIObursts.append(float(linha[4]))
                    elif linha[1] == 'DI':
                        self.duracaoIOburst.append(float(linha[2]))
                        self.duracaoIOburst.append(float(linha[3]))
                        self.duracaoIOburst.append(float(linha[4]))
                    elif linha[1] == 'DC':
                        self.duracaoCPUburst.append(float(linha[2]))
                        self.duracaoCPUburst.append(float(linha[3]))
                        self.duracaoCPUburst.append(float(linha[4]))

                # Dados das CPUs.
                elif linha[0] == 'C' and linha[1] == 'QT':
                    self.nCPUs = int(linha[2])

                # Dados da memória.
                elif linha[0] == 'M' and linha[1] == 'QT':
                    self.tamMemoria = int(linha[2])

                # Dados dos dispositivos.
                elif linha[0] == 'D' and linha[1] == 'QT':
                    self.nDispositivos = int(linha[2])
