# Sobre

Repositório para o desenvolvimento de um algoritmo líder-seguidor com PSO utilizando swarm intelligence para conclusão de curso.

## Pré-requisitos

Para conseguir executar este projeto é necessário ter instalado:

* [Python3](https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe)

#### (Caso esteja no Windows) Ao instalar o python lembre-se de marcar para adicionar Python ao Path
![python_install](https://files.realpython.com/media/win-install-dialog.40e3ded144b0.png)

* [Anaconda](https://www.anaconda.com/distribution/)

#### (Caso esteja no Windows) Ao instalar o python lembre-se de marcar para adicionar Anaconda ao Path
![anaconda_install](https://user-images.githubusercontent.com/1529481/27006849-a94d7958-4e05-11e7-903e-539b57b78709.png)

### Instalar bibliotecas pelo Anaconda:

1. Abra o Anaconda Navigator
1. Vá em Enviroments
1. Clique em base(root)
1. Pesquise por matplotlib (Caso não ache clique em Update Index)
1. Pesquise por numpy (Caso não ache clique em Update Index)
1. Instale os dois

### Instalar pelo site:

* [Matplotlib](https://anaconda.org/conda-forge/matplotlib).
* [Numpy](https://anaconda.org/conda-forge/numpy)

### Instalar Visual Studio Code no Anaconda:

1. Abra o Anaconda Navigator
1. Vá em Home
1. Clique para instalar o Visual Studio Code

### Instalar pelo site:

[Visual Studio Code](https://code.visualstudio.com/Download)

## Rodando o projeto

1. Abra o terminal e dê um clone no repositório.
1. Entre no Anaconda Navigator e dê launch no Visual Studio Code. 
1. Aperte F5 e aparecerá a opção de escolher quantas interações você deseja testar. 
1. Logo depois irá aparecer uma janela onde o mapa é apresentado e é atualizado a cada movimento do robô


## Lógica

A ideia é simular um mapa, para isso eu uso uma matriz onde eu defini as seguintes regras:
* Se posicão na matriz é igual a 0 = Campo vazio
* Se posicão na matriz é igual a 1 = Campo ocupado por robô
* Se posicão na matriz é igual a -1 = Alvo

* PSO utilizado se resume em três passos:
1. Primeiro passo: Mover particula no sentido da inercia;
1. Segundo passo: Pegar posição do vizinho de cada particula como o pbest dela e ir em direção a ele;
1. Terceiro passo: Pegar a média da posição do enxame como gbest de cada particula e ir em direção a ele.

![PSO](https://ljvmiranda921.github.io/assets/png/nn/pso_r_test1_zeroc1.gif)

## Diferença

Visto que o PSO tende a aglomerar as particulas em um ponto em comum elas nunca iriam ir ao caminho do alvo, visto isso eu fiz uma modificação na qual, localizo o robô que está mais perto do alvo e logo transformo ele no GBEST de todo o enxame e digo que o movimento das minhas particulas têm como prioridade ir para onde está o GBEST (que é o líder), ou seja, seria um líder-seguidor com PSO, com isso faço a comparação com o líder-seguidor sem PSO vs líder-seguidor com PSO, fazendo vários testes, com robôs posicionados em lugares diferentes, com alvo posicionado em lugares diferentes, com diferentes quantidades de particulas e quantidade de interações diferentes.


Qualquer dúvida entre em contato com este email: danielmessi13@hotmail.com

Se divirta!
