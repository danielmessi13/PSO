# -*- coding: utf-8 -*
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import time
# random.seed(30)
global velocidade, time_pause, gbest
velocidade = 1
time_pause = 0.0001
interacoes_com_pso = 0
interacoes_sem_pso = 0

# 0 = Baixo
# 90 = Direita
# 180 = Cima
# 270 = Esquerda


class Mapa():

    def __init__(self):
        self.mapa = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.alvo_achado = False

    # Cria o mapa com os robos e alvo de diferentes cores

    def criar(self, alvo, particulas):
        self.alvo_achado = True
        self.particula_lider = particulas[0]
        self.particula_lider.lider = True
        self.mapa[alvo[0]][alvo[1]] = 2
        self.alvo = alvo

        for i in particulas:
            self.mapa[i.posicao[0]][i.posicao[1]] = 1

            # Defino o líder (o que está mais perto do alvo)

            # Distancia do alvo para mim
            distancia_alvo_para_particula = self.calcula_distancia(
                i.posicao, self.alvo)

            # Distancia do líder para o alvo
            distancia_lider_para_alvo = self.calcula_distancia(
                self.alvo, self.particula_lider.posicao)

            # Se a distancia do alvo para mim for menor que a distancia do lider para o alvo,
            # significa que eu tenho que setar um novo líder, e tirar a liderança do outro
            if distancia_alvo_para_particula < distancia_lider_para_alvo:
                lider_x = self.alvo[0]
                lider_y = self.alvo[1]
                self.particula_lider.lider = False
                self.particula_lider = i
                self.particula_lider.gbest = [lider_x, lider_y]
                self.particula_lider.pbest = [lider_x, lider_y]
                i.lider = True

        global gbest

        gbest = self.particula_lider.posicao

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
                if i.lider == False:
                    i.gbest = [gbest[0], gbest[1]]
                else:
                    i.gbest = [self.alvo[0], self.alvo[1]]

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
        if particula.posicao != self.alvo:
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

    def limpar_espaco(self, particula):
        # Removo do mapa o lugar onde eu estava
        self.mapa[particula.posicao[0]][particula.posicao[1]] = 0

    def primeiro_movimento(self, particula):

        if particula.posicao != self.alvo:

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

    def atualizar_mapa(self, particula, posicao_antiga):
        if self.alvo == particula.posicao:
            # Se for o alvo muda pra cor diferente
            if particula.lider:
                self.mapa[particula.posicao[0]][particula.posicao[1]] = -1
                return 1
            else:
                self.mapa[posicao_antiga[0]][posicao_antiga[1]] = 1
                self.mapa[particula.posicao[0]][particula.posicao[1]] = -1
                return -1

            # Caso quando é o alvo

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

        # plt.imshow(self.mapa)
        # plt.plot()
        # plt.pause(time_pause)
        # plt.close()

        if particula.posicao[1] < particula.pbest[1]:
            self.mover_com_direcao(particula, "direita")
        elif particula.posicao[1] > particula.pbest[1]:
            self.mover_com_direcao(particula, "esquerda")

        # plt.imshow(self.mapa)
        # plt.plot()
        # plt.pause(time_pause)
        # plt.close()

    def terceiro_movimento(self, particula):

        if particula.posicao[0] < particula.gbest[0]:
            self.mover_com_direcao(particula, "baixo")
        elif particula.posicao[0] > particula.gbest[0]:
            self.mover_com_direcao(particula, "cima")

        # plt.imshow(self.mapa)
        # plt.plot()
        # plt.pause(time_pause)
        # plt.close()

        if particula.posicao[1] < particula.gbest[1]:
            self.mover_com_direcao(particula, "direita")
        elif particula.posicao[1] > particula.gbest[1]:
            self.mover_com_direcao(particula, "esquerda")

        # plt.imshow(self.mapa)
        # plt.plot()
        # plt.pause(time_pause)
        # plt.close()

    def mover_sem_pso(self, particulas):
        perto_do_alvo = [[self.alvo[0] + 1, self.alvo[1] + 1], [self.alvo[0] - 1, self.alvo[1] - 1],
                         [self.alvo[0] + 1, self.alvo[1] - 1], [self.alvo[0] - 1, self.alvo[1] + 1], [self.alvo[0] - 1, self.alvo[1]], [self.alvo[0], self.alvo[1] + 1], [self.alvo[0] + 1, self.alvo[1]], [self.alvo[0], self.alvo[1] - 1], ]

        for i in particulas:
            if (not i.lider and i.posicao not in perto_do_alvo) or (i.lider and i.posicao != self.alvo):

                # Se não estiver no alvo e for lider ou posicao nao esta perto e ele nao é lider
                # Primeiro movimento: Andar no sentido da inercia
                # na mesma orientacao em que esta
                if i.posicao != self.alvo:

                    # Terceiro movimento: Andar no sentido global
                    for j in range(5):
                        self.terceiro_movimento(i)

                    # Atualzia pbest e gbest
                    self.fitness(particulas)

    def mover(self, particulas):

        perto_do_alvo = [[self.alvo[0] + 1, self.alvo[1] + 1], [self.alvo[0] - 1, self.alvo[1] - 1],
                         [self.alvo[0] + 1, self.alvo[1] - 1], [self.alvo[0] - 1, self.alvo[1] + 1], [self.alvo[0] - 1, self.alvo[1]], [self.alvo[0], self.alvo[1] + 1], [self.alvo[0] + 1, self.alvo[1]], [self.alvo[0], self.alvo[1] - 1], ]

        for i in particulas:
            if (not i.lider and i.posicao not in perto_do_alvo) or (i.lider and i.posicao != self.alvo):

                # Se não estiver no alvo e for lider ou posicao nao esta perto e ele nao é lider
                # Primeiro movimento: Andar no sentido da inercia
                # na mesma orientacao em que esta
                if i.posicao != self.alvo:
                    for j in range(2):
                        self.primeiro_movimento(i)

                # plt.imshow(self.mapa)
                # plt.plot()
                # plt.pause(time_pause)
                # plt.close()

                # Segundo movimento: Andar no sentido dos seus vizinhos
                self.segundo_movimento(i)

                # Terceiro movimento: Andar no sentido global
                for j in range(3):
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

numero_de_particulas = int(input("Numero de particulas: "))
numero_interacoes = int(input("Numero de interacoes: "))
alvo = [random.randint(0, 17), random.randint(0, 17)]

particulas_sem_pso = []
particulas_com_pso = []

for i in range(numero_de_particulas):
    posicao_aleatoria = [random.randint(0, 16), random.randint(0, 16)]
    posicao_aleatoria_sem_pso = [posicao_aleatoria[0], posicao_aleatoria[1]]
    particulas_com_pso.append(Particula(posicao_aleatoria, alvo, "particula%s" % i))
    particulas_sem_pso.append(Particula(posicao_aleatoria_sem_pso, alvo, "particula%s" % i))

mapa = Mapa()
mapa.criar(alvo, particulas_com_pso)
mapa.fitness(particulas_com_pso)

mapa_sem_pso = Mapa()
mapa_sem_pso.criar(alvo, particulas_sem_pso)
mapa_sem_pso.fitness(particulas_sem_pso)

# plt.imshow(mapa.mapa)
# plt.plot()
# plt.pause(time_pause)
# plt.close()


comeco_pso = time.time()


plt.imshow(mapa.mapa)
plt.show()

for i in range(0, numero_interacoes):

    mapa.mover(particulas_com_pso)
    interacoes_com_pso += i

fim_pso = time.time()

print("COM PSO: ", round(comeco_pso - fim_pso, 2))


plt.imshow(mapa.mapa)
plt.show()

# plt.imshow(mapa_sem_pso.mapa)
# plt.plot()
# plt.pause(time_pause)
# plt.close()

plt.imshow(mapa.mapa)
plt.show()

comeco_sem_pso = time.time()

for j in range(0, numero_interacoes):
    mapa_sem_pso.mover_sem_pso(particulas_sem_pso)
    interacoes_sem_pso += j

fim_sem_pso = time.time()

print("SEM PSO: ", round(comeco_sem_pso - fim_sem_pso, 2))


plt.imshow(mapa_sem_pso.mapa)
plt.show()
