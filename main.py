from romenia import *
from copy import deepcopy


def Cria_Mapa_Romenia():
    # Inicializando Estados
    # Os valores Heuristicos são dados de acordo com a distância em linha reta de Bucharest
    # Os nós recebem o nome da estado e as coordenadas geográficas da estado

    Arad = Estado("Arad", 366)
    Bucharest = Estado("Bucharest", 0)
    Craiova = Estado("Craiova", 160)
    Drobreta = Estado("Drobreta", 242)
    Eforie = Estado("Eforie", 161)
    Fagaras = Estado("Fagaras", 178)
    Giurgiu = Estado("Giurgiu", 77)
    Hirsova = Estado("Hirsova", 151)
    Iasi = Estado("Iasi", 226)
    Lugoj = Estado("Lugoj", 244)
    Mehadia = Estado("Mehadia", 241)
    Neamt = Estado("Neamt", 234)
    Oradea = Estado("Oradea", 380)
    Pitesti = Estado("Pitesti", 98)
    Rimnicu_Vilcea = Estado("Rimnicu_Vilcea", 193)
    Sibiu = Estado("Sibiu", 253)
    Timisoara = Estado("Timisoara", 329)
    Urzineci = Estado("Urzineci", 80)
    Vaslui = Estado("Vaslui", 199)
    Zerind = Estado("Zerind", 374)

    # Estados de partida e destino
    Estado_Inicio = Arad
    Estado_Fim = Bucharest

    Estados = [Arad, Bucharest, Craiova, Drobreta, Eforie, Fagaras, Giurgiu, Hirsova, Iasi, Lugoj, Mehadia, Neamt,
               Oradea, Pitesti, Rimnicu_Vilcea, Sibiu, Timisoara, Urzineci, Vaslui, Zerind]

    # Monta a heuristica de acordo com a estado destino
    for estado in Estados:
        estado.gera_heuristica(Estado_Fim)
        print("{} - {}".format(estado.estado, estado.get_heuristica()))

    # Inicializando vizinhos
    Arad.vizinhos = [Vizinho(Zerind, 75), Vizinho(Sibiu, 140), Vizinho(Timisoara, 118)]
    Zerind.vizinhos = [Vizinho(Oradea, 71), Vizinho(Arad, 75)]
    Oradea.vizinhos = [Vizinho(Zerind, 71), Vizinho(Sibiu, 151)]
    Sibiu.vizinhos = [Vizinho(Oradea, 151), Vizinho(Arad, 140), Vizinho(Fagaras, 99), Vizinho(Rimnicu_Vilcea, 80)]
    Fagaras.vizinhos = [Vizinho(Sibiu, 99), Vizinho(Bucharest, 211)]
    Rimnicu_Vilcea.vizinhos = [Vizinho(Sibiu, 80), Vizinho(Pitesti, 97), Vizinho(Craiova, 146)]
    Pitesti.vizinhos = [Vizinho(Rimnicu_Vilcea, 97), Vizinho(Bucharest, 101), Vizinho(Craiova, 138)]
    Timisoara.vizinhos = [Vizinho(Arad, 118), Vizinho(Lugoj, 111)]
    Lugoj.vizinhos = [Vizinho(Timisoara, 111), Vizinho(Mehadia, 70)]
    Mehadia.vizinhos = [Vizinho(Lugoj, 70), Vizinho(Drobreta, 75)]
    Drobreta.vizinhos = [Vizinho(Mehadia, 75), Vizinho(Craiova, 120)]
    Craiova.vizinhos = [Vizinho(Drobreta, 120), Vizinho(Rimnicu_Vilcea, 146), Vizinho(Pitesti, 138)]
    Bucharest.vizinhos = [Vizinho(Fagaras, 211), Vizinho(Pitesti, 101), Vizinho(Giurgiu, 90), Vizinho(Urzineci, 85)]
    Giurgiu.vizinhos = [Vizinho(Bucharest, 90)]
    Urzineci.vizinhos = [Vizinho(Bucharest, 85), Vizinho(Hirsova, 98), Vizinho(Vaslui, 142)]
    Hirsova.vizinhos = [Vizinho(Urzineci, 98), Vizinho(Eforie, 86)]
    Eforie.vizinhos = [Vizinho(Hirsova, 86)]
    Vaslui.vizinhos = [Vizinho(Urzineci, 142), Vizinho(Iasi, 92)]
    Iasi.vizinhos = [Vizinho(Vaslui, 92), Vizinho(Neamt, 87)]
    Neamt.vizinhos = [Vizinho(Iasi, 87)]

    print("\n\n-----BUSCA HEURISTICA-----\n")
    # Calculando a rota
    Solucao = Rota(Estado_Inicio, Estado_Fim)
    print("melhor caminho:")
    print(*Solucao, sep=", ")

    print("\n\n------BUSCA GULOSA-----")
    gulosa = BuscaGulosa(Estado_Fim)
    gulosa.buscar(Estado_Inicio)


def Rota(Node_Inicio, Node_Fim):
    if Node_Fim.estado == Node_Inicio.estado:
        return [Node_Inicio]

    Fila_De_Rotas = []

    rota = Route(Node_Inicio)
    Fila_De_Rotas.append(rota)

    while True:
        melhores_ramos = []

        index_melhores_ramos = []

        # Encontra o melhor ramo entre os ramos abertos
        for rota in Fila_De_Rotas:
            custo_ramos = rota.custo_ramos()
            melhores_ramos.append(min(custo_ramos))
            index_melhores_ramos.append(custo_ramos.index(min(custo_ramos)))

        indice_melhor_rota = melhores_ramos.index(min(melhores_ramos))
        rota_com_melhor_ramo = deepcopy(Fila_De_Rotas[indice_melhor_rota])
        melhor_ramo = rota_com_melhor_ramo.ramos[index_melhores_ramos[indice_melhor_rota]]

        # Remove ramo da rota antiga
        rota = Fila_De_Rotas[indice_melhor_rota]
        rota.retira(melhor_ramo)

        rota_com_melhor_ramo.adiciona(melhor_ramo)
        Fila_De_Rotas.append(rota_com_melhor_ramo)

        # Adiciona uma nova rota ou remove uma rota que já acabou
        if len(rota.ramos) == 0:
            Fila_De_Rotas.remove(rota)

        # Condição de parada
        print(rota_com_melhor_ramo)
        if melhor_ramo.node.estado == Node_Fim.estado:
            break

    return rota_com_melhor_ramo.estados


class BuscaGulosa:
    def __init__(self, objetivo):
        self.fronteira = None
        self.objetivo = objetivo
        self.achou = False

    def buscar(self, atual):
        print("\nAtual: {}".format(atual.estado))
        atual.visitado = True

        if atual == self.objetivo:
            self.achou = True
        else:
            self.fronteira = VetorOrdenado(len(atual.vizinhos))
            for i in atual.vizinhos:
                if not i.node.visitado:
                    i.node.visitado = True
                    self.fronteira.inserir(i.node)
            self.fronteira.mostrar()
            if self.fronteira.getPrimeiro() is not None:
                BuscaGulosa.buscar(self, self.fronteira.getPrimeiro())


Cria_Mapa_Romenia()
