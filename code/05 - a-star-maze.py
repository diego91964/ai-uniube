from pyamaze import maze, agent
from queue import PriorityQueue



def heuristica (atual, destino):
    # Distância de manhattan
    xAtual = atual[0]
    yAtual = atual[1]
    xDestino = destino[0]
    yDestino = destino[1]
    return abs(xDestino - xAtual) + abs(yDestino - yAtual)

# f_score -> g_score + heuristica
# g_score -> Quantos passos já foram dados até chegar na célula

def a_star (labirinto, inicio):

    # Inicializar com o cálculo de custo infinito
    f_score = {celula : float("inf") for celula in labirinto.grid}

    g_score = {}

    g_score[inicio]  = 0

    f_score[inicio] = g_score[inicio] + heuristica(inicio,destino)
    #print(f_score)

    fila = PriorityQueue ()

    item = (f_score[inicio], heuristica(inicio,destino) , inicio)

    fila.put(item)

    #Armazenar o melhor caminho
    caminho_percorrido = {}
    todos_caminhos = {}

    while not fila.empty():
        celula = fila.get()[2]

        if celula == destino:
            break
        
        for direcao in "NSEW":
            if labirinto.maze_map[celula][direcao] == 1:
                linha_celula  = celula[0]
                coluna_celula = celula[1]

                if direcao == "N":
                    proxima_celula = (linha_celula - 1 , coluna_celula)
                elif direcao == "S":
                    proxima_celula = (linha_celula + 1 , coluna_celula)
                elif direcao == "E":
                    proxima_celula = (linha_celula  , coluna_celula + 1)
                elif direcao == "W":
                    proxima_celula = (linha_celula  , coluna_celula - 1)
                
                novo_g_score = g_score[celula]+1
                novo_f_score = novo_g_score + heuristica(proxima_celula,destino)

                if novo_f_score < f_score[proxima_celula]:
                    f_score[proxima_celula] = novo_f_score
                    g_score[proxima_celula] = novo_g_score
                    item = (novo_f_score , heuristica(proxima_celula,destino) , proxima_celula )
                    fila.put(item)
                    caminho_percorrido[proxima_celula] = celula
                    todos_caminhos [celula] = proxima_celula
    
    melhor_caminho = {}
    celula_analisada = destino
    while celula_analisada != inicio:
        melhor_caminho[caminho_percorrido[celula_analisada]] = celula_analisada
        celula_analisada = caminho_percorrido[celula_analisada]

    #print(caminho_percorrido)
    #print(melhor_caminho)
    return melhor_caminho

        


labirinto = maze(20,20)
labirinto.CreateMaze()

f_score = {celula : float("inf") for celula in labirinto.grid}


agente = agent(labirinto , filled = True , footprints = True)

inicio = (labirinto.rows, labirinto.cols)
destino = (1,1)

print (labirinto.maze_map)

print(labirinto.grid)

caminho = a_star(labirinto, inicio)

print(caminho)

labirinto.tracePath({agente : caminho} , delay=100)

labirinto.run()
