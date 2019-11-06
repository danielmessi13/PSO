# -*- coding: utf-8 -*
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import time
# random.seed(30)
global velocidade, time_pause
velocidade = 1
time_pause = 0.1

# 0 = Baixo
# 90 = Direita
# 180 = Cima
# 270 = Esquerda


class Mapa():

    def __init__(self):
        self.mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.alvo_achado = False

    # Cria o mapa com os robos e alvo de diferentes cores

    def criar(self, alvo, particulas):
        for i in particulas:
            self.mapa[i.posicao[0]][i.posicao[1]] = 1

        self.mapa[alvo[0]][alvo[1]] = 2
        self.alvo = alvo

    # Calcula a distancia entre dois pontos
    def calcula_distancia(self, posicao, posicao_alvo):
        return math.sqrt((posicao[0] - posicao_alvo[0])**2 +
                         (posicao[1] - posicao_alvo[1])**2)

    # Atualiza pbest
    def fitness(self, particulas):
        self.pbest(particulas)
        self.gbest(particulas)

    def gbest(self, particulas):
        posicoes = []

        if self.alvo_achado:
            # Se tiver achado o alvo já, mudar 
            for i in particulas:
                if i.lider == True:
                    i.gbest = [i.posicao[0], i.posicao[1]]
        else:
            # Pego as posicoes das particulas
            for i in particulas:
                posicoes.append(i.posicao)

            # Media das posicoes para calcular gbest
            media = np.around(np.average(posicoes, axis=0))

            # Atribui gbest para as particulas
            for i in particulas:
                i.gbest = media

    def mover_com_direcao(self, particula, direcao):
        posicao_antiga = [particula.posicao[0], particula.posicao[1]]

        self.limpar_espaco(particula)

        if direcao == "cima":
            particula.posicao[0] -= velocidade
            particula.orientacao = 180
        elif direcao == "baixo":
            particula.posicao[0] += velocidade
            particula.orientacao = 0
        elif direcao == "direita":
            particula.posicao[1] += velocidade
            particula.orientacao = 90
        else:
            particula.posicao[1] -= velocidade
            particula.orientacao = 270

        retorno = self.atualizar_mapa(particula, posicao_antiga)

        if retorno == 0 or retorno == -1:
            particula.posicao[0] = posicao_antiga[0]
            particula.posicao[1] = posicao_antiga[1]

        elif retorno == 1:
            self.alvo_achado = True
            particula.lider = True
        

    def limpar_espaco(self, particula):
        # Removo do mapa o lugar onde eu estava
        self.mapa[particula.posicao[0]][particula.posicao[1]] = 0

    def primeiro_movimento(self, particula):
        # Salvo a posição antiga para caso eu vá para um lugar que
        # já tenha um robô, simulando que eles não podem se bater
        posicao_antiga = [particula.posicao[0], particula.posicao[1]]
        self.limpar_espaco(particula)

        # Verifica qual sentido ele está, e move neste sentido

        if particula.orientacao == 180:
            # Cima
            particula.posicao[0] -= velocidade

            # Se tiver no limite do topo vai para a direita
            if particula.posicao[0] < 0:
                particula.posicao[0] = 0
                particula.posicao[1] += velocidade
                particula.orientacao = 90

        elif particula.orientacao == 0:
            # Baixo
            particula.posicao[0] += velocidade

            # Se estiver no limite de baixo vai para a esquerda
            if particula.posicao[0] == 10:
                particula.posicao[0] = 9
                particula.posicao[1] -= velocidade
                particula.orientacao = 270

        elif particula.orientacao == 90:
            # Direita
            particula.posicao[1] += velocidade

            # Se estiver no limite da direita vai para baixo
            if particula.posicao[1] == 10:
                particula.posicao[1] = 9
                particula.posicao[0] += velocidade
                particula.orientacao = 0

        else:
            # Esquerda
            particula.posicao[1] -= velocidade

            # Se estiver no limite da esquerda vai para cima
            if particula.posicao[1] < 0:
                particula.posicao[1] = 0
                particula.posicao[0] -= velocidade
                particula.orientacao = 180

        # Apos me mover altero no mapa o lugar onde eu estava
        retorno = self.atualizar_mapa(particula, posicao_antiga)

        if retorno == 0 or retorno == -1:
            particula.posicao[0] = posicao_antiga[0]
            particula.posicao[1] = posicao_antiga[1]

        elif retorno == 1:
            self.alvo_achado = True
            particula.lider = True

    def atualizar_mapa(self, particula, posicao_antiga):
        if self.alvo == particula.posicao:
            # Se for o alvo muda pra cor diferente
            self.mapa[particula.posicao[0]][particula.posicao[1]] = -1
            # Caso quando é o alvo
            return -1
        elif (self.mapa[particula.posicao[0]][particula.posicao[1]] == 1):
            self.mapa[particula.posicao[0]][particula.posicao[1]] = 1
            self.mapa[posicao_antiga[0]][posicao_antiga[1]] = 1
            # Caso quando ja existe robo la
            return 0
        else:
            self.mapa[particula.posicao[0]][particula.posicao[1]] = 1
            # Caso normal
            return 1

    def segundo_movimento(self, particula):

        if particula.posicao[0] < particula.pbest[0]:
            self.mover_com_direcao(particula, "baixo")
        elif particula.posicao[0] > particula.pbest[0]:
            self.mover_com_direcao(particula, "cima")

        plt.imshow(self.mapa)
        plt.plot()
        plt.pause(time_pause)
        plt.close()

        if particula.posicao[1] < particula.pbest[1]:
            self.mover_com_direcao(particula, "direita")
        elif particula.posicao[1] > particula.pbest[1]:
            self.mover_com_direcao(particula, "esquerda")

        plt.imshow(self.mapa)
        plt.plot()
        plt.pause(time_pause)
        plt.close()

    def terceiro_movimento(self, particula):
        if particula.posicao[0] < particula.gbest[0]:
            self.mover_com_direcao(particula, "baixo")
        elif particula.posicao[0] > particula.gbest[0]:
            self.mover_com_direcao(particula, "cima")

        plt.imshow(self.mapa)
        plt.plot()
        plt.pause(time_pause)
        plt.close()

        if particula.posicao[1] < particula.gbest[1]:
            self.mover_com_direcao(particula, "direita")
        elif particula.posicao[1] > particula.gbest[1]:
            self.mover_com_direcao(particula, "esquerda")

        plt.imshow(self.mapa)
        plt.plot()
        plt.pause(time_pause)
        plt.close()

    def mover(self, particulas):
        for i in particulas:
            if i.posicao != self.alvo:
                # Primeiro movimento: Andar no sentido da inercia
                # na mesma orientacao em que esta
                self.primeiro_movimento(i)

                plt.imshow(self.mapa)
                plt.plot()
                plt.pause(time_pause)
                plt.close()

                # Segundo movimento: Andar no sentido dos seus vizinhos
                self.segundo_movimento(i)

                # Terceiro movimento: Andar no sentido global
                self.terceiro_movimento(i)

                # Atualzia pbest e gbest
                self.fitness(particulas)

    def pbest(self, particulas):
        for i in particulas:
            for j in particulas:

                # Se nao tiver pbest, eu pego o meu primeira particula existente
                # caso nao haja mais, fica como essa, caso haja altera no for
                if i.pbest == [-1, -1] and i.nome != j.nome:

                    # Nao podemos atribuir direto i.pest = j.posicao pois em python eles irao ter
                    # a mesma referencia, entao se eu mudasse a posicao do j ele mudaria tambem o
                    # pbest
                    pbest_x = j.posicao[0]
                    pbest_y = j.posicao[1]
                    i.pbest = [pbest_x, pbest_y]

                # Se nao for a mesma particula, e já nao está como default, entra no if
                if i.nome != j.nome:

                    # Distancia da particula para mim
                    distancia_particula_para_mim = self.calcula_distancia(
                        i.posicao, j.posicao)

                    # Distancia da particula para o pbest
                    distancia_particula_para_pbest = self.calcula_distancia(
                        i.posicao, i.pbest)

                    # Se a distancia para mim for menor que o pbest,
                    # significa que meu pbest agora é a posicao daquela particula
                    if distancia_particula_para_mim < distancia_particula_para_pbest:

                        # Nao podemos atribuir direto i.pest = j.posicao pois em python eles irao ter
                        # a mesma referencia, entao se eu mudasse a posicao do j ele mudaria tambem o
                        # pbest
                        pbest_x = j.posicao[0]
                        pbest_y = j.posicao[1]
                        i.pbest = [pbest_x, pbest_y]


class Particula():

    # gbest = Melhor posicao dentre todas as particulas
    # fitness = Funcao que faz avalicao de qual o melhor pbest e gbest
    def __init__(self, posicao, posicao_alvo, nome):
        self.nome = nome
        self.posicao = posicao
        self.posicao_alvo = posicao_alvo
        self.orientacao = random.choice([0, 90, 180, 270])
        self.gbest = []
        self.lider = False
        # ERRADO: pbest = Melhor posicao que a particula ja esteve
        # CERTO: pbest = Melhor posicao levando em consideracao os vizinhos da particula
        self.pbest = [-1, -1]

        # Terceiro passo = Me mover no sentido
        # da minha melhor posicao


# Preciso sempre calcular a distancia
# Entre a particula e o alvo

# numero_de_particulas = int(input("Numero de particulas: "))
numero_interacoes = int(input("Numero de interacoes: "))
alvo = [random.randint(0, 9), random.randint(0, 9)]
posicao = [random.randint(0, 9), random.randint(0, 9)]
posicao2 = [random.randint(0, 9), random.randint(0, 9)]
posicao3 = [random.randint(0, 9), random.randint(0, 9)]
posicao4 = [random.randint(0, 9), random.randint(0, 9)]
posicao5 = [random.randint(0, 9), random.randint(0, 9)]

# alvo = [9, 9]
# posicao = [5, 5]
# posicao2 = [1, 1]
# posicao3 = [7, 7]

# target_error = float(input("Inform the target error: "))

# No for terei que ter uma lista com a distancia de cada particula
# para o alvo
# print("Alvo: %s" % alvo)

particula1 = Particula(posicao, alvo, "particula1")
particula2 = Particula(posicao2, alvo, "particula2")
particula3 = Particula(posicao3, alvo, "particula3")
particula4 = Particula(posicao4, alvo, "particula3")
particula5 = Particula(posicao5, alvo, "particula3")
particulas = [particula1, particula2, particula3, particula4, particula5]
mapa = Mapa()
mapa.criar(alvo, particulas)
mapa.fitness(particulas)

plt.imshow(mapa.mapa)
plt.plot()
plt.pause(time_pause)
plt.close()

# print("Posicao: " + str(particula1.posicao))
# print("Alvo: " + str(particula1.posicao_alvo))
# print("Orientacao: " + str(particula1.orientacao))
# print("Pbest: " + str(particula1.pbest))

# print("Posicao2: " + str(particula2.posicao))
# print("Alvo2: " + str(particula2.posicao_alvo))
# print("Orientacao2: " + str(particula2.orientacao))
# print("Pbest2: " + str(particula2.pbest))

# print("Posicao3: " + str(particula3.posicao))
# print("Alvo3: " + str(particula3.posicao_alvo))
# print("Orientacao3: " + str(particula3.orientacao))
# print("Pbest3: " + str(particula3.pbest))


for i in range(0, numero_interacoes):
    mapa.mover(particulas)


# print("Posicao: " + str(particula1.posicao))
# print("Alvo: " + str(particula1.posicao_alvo))
# print("Orientacao: " + str(particula1.orientacao))
# print("Pbest: " + str(particula1.pbest))

# print("Posicao2: " + str(particula2.posicao))
# print("Alvo2: " + str(particula2.posicao_alvo))
# print("Orientacao2: " + str(particula2.orientacao))
# print("Pbest2: " + str(particula2.pbest))

# print("Posicao3: " + str(particula3.posicao))
# print("Alvo3: " + str(particula3.posicao_alvo))
# print("Orientacao3: " + str(particula3.orientacao))
# print("Pbest3: " + str(particula3.pbest))


# print("Posicao: " + str(particula1.posicao))
# print("Alvo: " + str(particula1.posicao_alvo))
# print("Orientacao: " + str(particula1.orientacao))
# print("Pbest: " + str(particula1.pbest))

# print("Posicao2: " + str(particula2.posicao))
# print("Alvo2: " + str(particula2.posicao_alvo))
# print("Orientacao2: " + str(particula2.orientacao))
# print("Pbest2: " + str(particula2.pbest))

# print("Posicao3: " + str(particula3.posicao))
# print("Alvo3: " + str(particula3.posicao_alvo))
# print("Orientacao3: " + str(particula3.orientacao))
# print("Pbest3: " + str(particula3.pbest))

""" print(mapa) """
