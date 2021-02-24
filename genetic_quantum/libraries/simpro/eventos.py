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

import os
from math import *
import random

from .colecoes import Colecoes
from .fila import Fila
#from .escalonador import Escalonador, PRTY, FCFS, RR, SJF, SRT, FPCS, IFCS, PFCS
from .escalonador import *
from .load import Cenario
from .plot import Plot
from .cpu import CPU
from .processo import Processo
from .dispositivo import Dispositivo

#from numba import jit
#import warnings
#warnings.filterwarnings('ignore')

class Evento():
    ''' Class docstring.'''

    def __init__(self, escalonador, arquivo, modelo):
        self.cenario = Cenario()
        self.arquivo = arquivo
        self.escalonador = escalonador
        self.modelo = modelo

        self.quantum = self.escalonador.getQuantum()

        self.preemptivo = self.escalonador.getPreemp()
        self.colecao = Colecoes()

        self.tempoSimulacao = 0.0

        # Indicadores.
        self.throughput = 0
        self.turnaround = 0.0
        self.esperaTotal = 0.0

        self.filaDeProntos = Fila()

        self.plot = Plot()

    def start(self):
        ''' Method docstring.'''

        fel = []
        self.cenario.carregaCenario(self.arquivo, self.modelo)

        # Modelo DETERMINISTICO.
        if self.modelo == 'D':
            cpu = CPU(1)
            self.colecao.CPUs.append(cpu)

            #cria processos
            for n in self.cenario.listaDeProcessos:
                p = Processo(None, self.quantum, None, None, None, None, None, None, n)
                self.colecao.Processos.append(p)

            for processo in self.colecao.Processos:
                chegadaProcesso = processo.getChegada()
                fel.append([1, chegadaProcesso, processo.getProcessoId()])

        # Modelo PROBABILISTICO.
        elif self.modelo == 'P':
            self.tempoSimulacao = self.cenario.tempoSimulacao

            # Povoa coleção de CPUs.
            for i in range(1, self.cenario.nCPUs+1):
                cpu = CPU(i)
                self.colecao.CPUs.append(cpu)

            # Povoa colecao de Dispositivos.
            for i in range(1, self.cenario.nDispositivos+1):
                dispositivo = Dispositivo(i)
                self.colecao.Dispositivos.append(dispositivo)
            tempClock = 0

            # Realiza as chegadas de processos.
            while tempClock <= self.tempoSimulacao:
                chegadaProcesso = int(random.expovariate(1/float(self.cenario.tempoChegadaProcesso)))
                tempClock = tempClock + chegadaProcesso
                # Inicializa FEL com chegadas de processos.
                fel.append([1, tempClock, None])

        return fel

    # Evento 1.
    def fimChegadaProcessoCPU(self, tempo, processoId):
        ''' Method docstring.'''

        fel = []
        cpu = CPU()

        # Utilização da CPU no momento atual.
        for c in self.colecao.CPUs:
            c.insereUtilizacaoAtual(tempo)

        if self.modelo == 'D':
            p = self.colecao.buscaProcesso(processoId)
            # Ocorre quando dois processos chegam ao mesmo tempo.

        elif self.modelo == 'P':
            self.colecao.nProcessos += 1
            ident = self.colecao.nProcessos
            if self.cenario.nDispositivos != 0:
                dispositivo = random.randint(1, self.cenario.nDispositivos)
            else:
                dispositivo = None

            p = Processo(
                ident, self.quantum, self.cenario.nIObursts,
                self.cenario.duracaoIOburst, self.cenario.duracaoCPUburst,
                dispositivo, tempo, self.cenario.prioridade)
            # Adiciona o processo a coleção.
            #print("Processo criado:", p)
            self.colecao.Processos.append(p)

        emExecucao, cpu = self.escalonador.desempate(p, self.colecao)
        if emExecucao != None:
            self.filaDeProntos.insert(emExecucao)
            fel.append([0, emExecucao.getProcessoId(), 1])
            emExecucao.setTerminoExecucao(tempo)
            emExecucao.recalculaExecucao()
            cpu.setDisponivel(True)

        self.filaDeProntos.insert(p)
        # Existe CPU disponível?
        cpu = self.colecao.buscaCpuLivre()
        # Verifica se foi encontrada uma CPU livre.
        if cpu != None:
            processo = self.escalonador.selecionaProcesso(self.filaDeProntos, tempo)
            #agenda na fel ([eventoID,tempo,processoID,cpuID])
            # O processo esperou desde o fim da última execução até agora.

            processo.incEspera(tempo)
            processo.setInicioExecucao(tempo)
            cpu.setInicioExecucao(tempo)
            #verificar se o quantum e menor ou maior que o burst atual
            #print("------------------------------> processo ID:", processo.processoId)
            if (self.quantum != None) and (self.quantum <= processo.getCpuBurstAtual()):
                fel.append([2, (tempo+self.quantum), processo.getProcessoId(), cpu.getCpuId()])
                processo.setTerminoExecucao(tempo+self.quantum)
                cpu.setTerminoExecucao(tempo+self.quantum)
            else:
                fel.append([2, (tempo+processo.getCpuBurstAtual()), processo.getProcessoId(), cpu.getCpuId()])
                processo.setTerminoExecucao(tempo+processo.getCpuBurstAtual())
                cpu.setTerminoExecucao(tempo+processo.getCpuBurstAtual())
            processo.insereExecucao()
            cpu.insereExecucao()
            #reserva CPU
            cpu.setDisponivel(False)
            cpu.incOciosidade(tempo) #incrementa o tempo que a cpu ficou livre
            #atribui processo a cpu
            cpu.setProcessoAtual(processo.getProcessoId())
            return fel

        #----------------------------------------------------------#
        if (self.preemptivo == True) and (not self.filaDeProntos.empty()):
            #invoca escalonador e recalcula escala
            novo, processoInterrompido, cpuInterrompida = self.escalonador.recalcula(self.filaDeProntos, self.colecao, tempo)
            if novo != None: #sugere mudanca?
                #####################
                #interrompe processo#
                #####################
                #retira processo (em execução) da fel
                fel.append([0,processoInterrompido.getProcessoId(),cpuInterrompida.getCpuId()])
                processoInterrompido.setTerminoExecucao(tempo)
                processoInterrompido.recalculaExecucao()
                cpuInterrompida.setTerminoExecucao(tempo)
                cpuInterrompida.recalculaExecucao()
                #reduz o burst que estava em execucao
                processoInterrompido.reduzCpuBurst(tempo)
                cpuInterrompida.setDisponivel(True)
                cpuInterrompida.incExecucao(tempo)
                #reserva cpu para o novo processo
                cpuInterrompida.setDisponivel(False)
                cpuInterrompida.incOciosidade(tempo)
                cpuInterrompida.setProcessoAtual(novo.getProcessoId())
                #insere interrompido na fila de prontos
                self.filaDeProntos.insert(processoInterrompido)
                #agenda o novo processo na fel
                novo.incEspera(tempo) #O processo esperou desde o fim da ultima execucao ate agora.
                fel.append([2, (tempo+novo.getCpuBurstAtual()), novo.getProcessoId(), cpuInterrompida.getCpuId()])
                novo.setInicioExecucao(tempo)
                cpuInterrompida.setInicioExecucao(tempo)
                novo.setTerminoExecucao(tempo+novo.getCpuBurstAtual())
                cpuInterrompida.setTerminoExecucao(tempo+novo.getCpuBurstAtual())
                novo.insereExecucao()
                cpuInterrompida.insereExecucao()
                return fel
            else:
                return fel
        else:
            return fel

    # Evento 2.
    def fimExecutaCPU(self, tempo, processoId, cpuId):
        ''' Method docstring.'''

        fel = []

        cpu = self.colecao.buscaCpu(cpuId)

        #Utilizacao da cpu no momento atual
        for c in self.colecao.CPUs:
            c.insereUtilizacaoAtual(tempo)

        processo = self.colecao.buscaProcesso(processoId)
        processo.incExecucao(tempo)

        if self.quantum != None:
            # No metodo RR, o burst apenas executa durante o tempo de quantum, e não até o fim.
            # Assim, ao fim da execeução da CPU, o processo deve voltar para a fila de prontos.
            # Caso o burst encerre, se inicia uma execução IO. TODO: Ver como implementar isso.

            #reduz burst (True = Reduziu burst) (False = Decrementou)                      # Chamou aqui.
            if processo.subQuantum():
                #processo volta para a fila de prontos
                self.filaDeProntos.insert(processo)
                #Existe processo aguardando execucao?
                if not self.filaDeProntos.empty(): #Fila de prontos não vazia
                    novoProcesso = self.escalonador.selecionaProcesso(self.filaDeProntos, tempo)
                    #agenda na fel
                    novoProcesso.incEspera(tempo) #O processo esperou desde o fim da ultima execucao ate agora.
                    novoProcesso.setInicioExecucao(tempo)
                    cpu.setInicioExecucao(tempo)
                    if self.quantum <= novoProcesso.getCpuBurstAtual():
                        fel.append([2, (tempo+self.quantum), novoProcesso.getProcessoId(), cpu.getCpuId()])
                        novoProcesso.setTerminoExecucao(tempo+self.quantum)
                        cpu.setTerminoExecucao(tempo+self.quantum)
                    else:
                        fel.append([2, (tempo+novoProcesso.getCpuBurstAtual()), novoProcesso.getProcessoId(), cpu.getCpuId()])
                        novoProcesso.setTerminoExecucao(tempo+novoProcesso.getCpuBurstAtual())
                        cpu.setTerminoExecucao(tempo+novoProcesso.getCpuBurstAtual())
                    novoProcesso.insereExecucao()
                    cpu.insereExecucao()
                    cpu.setDisponivel(True)
                    cpu.incExecucao(tempo)
                    # Nesse meio tempo a CPU sai de um processo e vai pra outro.
                    # É necessário incrementar a execução referente ao processo anterior.
                    cpu.setDisponivel(False)
                    # A ociosidade será incrementada em zero.
                    cpu.incOciosidade(tempo)
                    cpu.setProcessoAtual(novoProcesso.getProcessoId())
                else:
                    # Fila de prontos vazia.
                    # Libera CPU.
                    cpu.setDisponivel(True)
                    cpu.incExecucao(tempo)

                return fel
        else:
            #print("-------------------------- NÃO É ROUND ROBIN!")
            processo.decrementaCpuBursts()

        # Ou o processo encerra, ou executa IO.
        if processo.getnCpuBursts() == 0: #Ultimo burst? Sim

            if self.modelo == 'D':
                encerraProcesso = 0

            elif self.modelo == 'P':
                if self.cenario.tempoEncProcesso[1] == 0 or self.cenario.tempoEncProcesso[2] == 0:
                    encerraProcesso = 0
                else:
                    encerraProcesso = int(random.triangular(self.cenario.tempoEncProcesso[0], self.cenario.tempoEncProcesso[2], self.cenario.tempoEncProcesso[1]))

            # Agenda na FEL.
            fel.append([4, (tempo+encerraProcesso), processo.getProcessoId()])

        else: #Nao, então IO
            dispositivoId = processo.getDispositivo()
            dispositivo = self.colecao.buscaDispositivo(dispositivoId)
            if dispositivo.getDisponivel():
                dispositivo.setDisponivel(False) #reserva dispositivo para o processo
                dispositivo.setProcessoAtual(processo.getProcessoId())
                # Agenda na FEL.
                fel.append([3, (tempo+processo.getIoBurstAtual()), processo.getProcessoId()])
            else:
                dispositivo.filaIO.insert(processo)

        # Existe processo aguardando execução?
        if not self.filaDeProntos.empty():
            # Fila de prontos não vazia.
            novoProcesso = self.escalonador.selecionaProcesso(self.filaDeProntos,tempo)
            #agenda na fel
            novoProcesso.incEspera(tempo) #O processo esperou desde o fim da ultima execucao ate agora.
            novoProcesso.setInicioExecucao(tempo)
            cpu.setInicioExecucao(tempo)
            if (self.quantum is not None) and (self.quantum <= novoProcesso.getCpuBurstAtual()):
                fel.append([2, (tempo+self.quantum), novoProcesso.getProcessoId(), cpu.getCpuId()])
                novoProcesso.setTerminoExecucao(tempo+self.quantum)
                cpu.setTerminoExecucao(tempo+self.quantum)
            else:
                fel.append([2, (tempo+novoProcesso.getCpuBurstAtual()), novoProcesso.getProcessoId(), cpu.getCpuId()])
                novoProcesso.setTerminoExecucao(tempo+novoProcesso.getCpuBurstAtual())
                cpu.setTerminoExecucao(tempo+novoProcesso.getCpuBurstAtual())
            novoProcesso.insereExecucao()
            cpu.insereExecucao()
            cpu.setDisponivel(True)
            cpu.incExecucao(tempo)
            # Nesse meio tempo a cpu sai de um processo e vai pra outro.
            # É necessário incrementar a execução referente ao processo anterior.
            cpu.setDisponivel(False)
            # A ociosidade será incrementada em zero.
            cpu.incOciosidade(tempo)
            cpu.setProcessoAtual(novoProcesso.getProcessoId())
        else:
            # Fila de prontos vazia.
            # Libera CPU.
            cpu.setDisponivel(True)
            cpu.incExecucao(tempo)
        
        return fel

    # Evento 3.
    def fimExecutaIO(self, tempo, processoId):
        ''' Method docstring.'''

        fel = []
        cpu = CPU()

        # Utilização da CPU no momento atual.
        for c in self.colecao.CPUs:
            c.insereUtilizacaoAtual(tempo)

        processo = self.colecao.buscaProcesso(processoId)

        processo.decrementaIoBursts()
        processo.setAuxiliar(tempo)

        dispositivoId = processo.getDispositivo()
        dispositivo = self.colecao.buscaDispositivo(dispositivoId)

        # No fim do IO, sera executado um CPU burst.
        if processo.getnCpuBursts() == 0: # Último burst? (sim)

            if self.modelo == 'D':
                encerraProcesso = 0

            elif self.modelo == 'P':
                if self.cenario.tempoEncProcesso[1] == 0 or self.cenario.tempoEncProcesso[2] == 0:
                    encerraProcesso = 0
                else:
                    encerraProcesso = int(random.triangular(self.cenario.tempoEncProcesso[0], self.cenario.tempoEncProcesso[2], self.cenario.tempoEncProcesso[1]))
            # Agenda na FEL.
            fel.append([4, (tempo+encerraProcesso), processo.getProcessoId()])

        else: #não
            #Busca uma CPU que esteja livre.
            cpu = self.colecao.buscaCpuLivre()
            # Caso encontre CPU livre.
            if cpu is not None:
                # Agenda na FEL.
                processo.setInicioExecucao(tempo)
                cpu.setInicioExecucao(tempo)
                if (self.quantum is not None) and (self.quantum <= processo.getCpuBurstAtual()):
                    fel.append([2, (tempo+self.quantum), processo.getProcessoId(), cpu.getCpuId()])
                    processo.setTerminoExecucao(tempo+self.quantum)
                    cpu.setTerminoExecucao(tempo+self.quantum)
                else:
                    fel.append([2, (tempo+processo.getCpuBurstAtual()), processo.getProcessoId(), cpu.getCpuId()])
                    processo.setTerminoExecucao(tempo+processo.getCpuBurstAtual())
                    cpu.setTerminoExecucao(tempo+processo.getCpuBurstAtual())
                processo.insereExecucao()
                cpu.insereExecucao()
                # Reserva CPU para o processo.
                cpu.setDisponivel(False)
                cpu.incOciosidade(tempo)
                cpu.setProcessoAtual(processo.getProcessoId())
            else:
                self.filaDeProntos.insert(processo)

        #----------------------------------------------------------#
        if self.preemptivo and not self.filaDeProntos.empty():
            #invoca escalonador e recalcula escala
            novo, processoInterrompido, cpuInterrompida = self.escalonador.recalcula(self.filaDeProntos, self.colecao, tempo)
            if novo is not None: #sugere mudanca?:
                #####################
                #interrompe processo#
                #####################
                #retira processo (em execução) da fel
                fel.append([0, processoInterrompido.getProcessoId(), cpuInterrompida.getCpuId()])
                processoInterrompido.setTerminoExecucao(tempo)
                processoInterrompido.recalculaExecucao()
                cpuInterrompida.setTerminoExecucao(tempo)
                cpuInterrompida.recalculaExecucao()
                #reduz o burst que estava em execucao
                processoInterrompido.reduzCpuBurst(tempo)
                #reserva cpu para o novo processo
                cpuInterrompida.setDisponivel(True)
                cpuInterrompida.incExecucao(tempo)
                #reserva cpu para o novo processo
                cpuInterrompida.setDisponivel(False)
                cpuInterrompida.incOciosidade(tempo)
                cpuInterrompida.setProcessoAtual(novo.getProcessoId())
                #insere interrompido na fila de prontos
                self.filaDeProntos.insert(processoInterrompido)
                #agenda o novo processo na fel
                fel.append([2, (tempo+novo.getCpuBurstAtual()), novo.getProcessoId(), cpuInterrompida.getCpuId()])
                novo.setInicioExecucao(tempo)
                cpuInterrompida.setInicioExecucao(tempo)
                novo.setTerminoExecucao(tempo+novo.getCpuBurstAtual())
                cpuInterrompida.setTerminoExecucao(tempo+novo.getCpuBurstAtual())
                novo.insereExecucao()
                cpuInterrompida.insereExecucao()
        #Apos o termino dos agendamentos referentes ao processo atual,
        #a fila do dispositivo é verificada
        if not dispositivo.filaIO.empty():
            # Fila não vazia.
            novoProcesso = dispositivo.filaIO.remove()
            # Eeserva dispositivo para o processo.
            dispositivo.setDisponivel(False)
            dispositivo.setProcessoAtual(processo.getProcessoId())
            #agenda na fel
            fel.append([3, (tempo+novoProcesso.getIoBurstAtual()), novoProcesso.getProcessoId()])
        else: #Fila Vazia
            dispositivo.setDisponivel(True)

        return fel

    # Evento 4.
    def fimEncerraProcesso(self, tempo, processoId):
        ''' Method docstring.'''

        fel = []

        # Utilização da CPU no momento atual.
        for c in self.colecao.CPUs:
            c.insereUtilizacaoAtual(tempo)

        self.throughput += 1
        processo = self.colecao.buscaProcesso(processoId)

        self.turnaround += tempo - processo.getChegada()
        self.esperaTotal += processo.getTempoEspera()

        self.colecao.finalizaProcesso(processoId)

        return fel

    def fim_execucao(self, tempo):
        ''' Method docstring.'''

        esperaExtra = 0
        cont = 0
        for p in self.colecao.Processos:
            cont += 1
            if p.getTempoExecucao() == 0:
                esperaExtra += tempo - p.getChegada()
            else:
                esperaExtra += p.getTempoEspera()

        if cont != 0:
            esperaExtra = esperaExtra/cont

        if self.modelo == 'D':
            self.tempoSimulacao = tempo

        execucaoCPus = 0

        for cpu in self.colecao.CPUs:
            execucaoCPus += (self.tempoSimulacao - cpu.getTotalOciosidade())
        if self.throughput == 0:
            tput = 0
            taround = 0
            usamcpu = ((execucaoCPus/len(self.colecao.CPUs))/tempo)*100
            tespera = 0
        else:
            tput = self.throughput
            taround = self.turnaround/self.throughput
            usamcpu = ((execucaoCPus/len(self.colecao.CPUs))/tempo)*100
            tespera = (self.esperaTotal/self.throughput) + esperaExtra

        # Output the results


        root_path = os.getcwd()
        results_folder = root_path + "\\resources\\SimPro-results\\"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        # Slicing the file name to get the scenario name
        scenario_name = str(self.arquivo).rsplit('/', 1)[1].rsplit('.', 1)[0]


        result_file_name = results_folder + scenario_name + "_results.txt"

        file = open(result_file_name, 'a')

        text = ""
        if os.stat(result_file_name).st_size == 0:
            text = 'THROUGHPUT\tTURNAROUND\tUTILIZACAO\tESPERA\n'
        text += str(float(tput)) + '\t' + str(taround) + '\t' + str(usamcpu) + '\t' + str(tespera) + '\n'
        file.write(text)
        file.close()
