class Estado:

    def __init__(self, nome_estado, valor_heuristico):
        self.estado = nome_estado
        self.heuristica = valor_heuristico
        self.vizinhos = []

    def __init__(self, nome_stado, distancia):
        self.estado = nome_stado
        self.distancia = distancia
        self.heuristica = 0
        self.vizinhos = []
        self.visitado = False

    def gera_heuristica(self, estado_alvo):
        self.heuristica = self.distancia - estado_alvo.distancia

    def get_heuristica(self):
        return self.heuristica

    def get_distancia(self):
        return self.distancia

    def __str__(self):
        return self.estado


class Vizinho:
    def __init__(self, estado_alvo, valor_custo):
        self.node = estado_alvo
        self.distancia = valor_custo

    def custo(self):
        return self.distancia + self.node.heuristica


class Route:
    def __init__(self, estado_inicial):
        self.distancias = 0
        # estados avaliadas
        self.estados = [estado_inicial]
        # estados ainda não avaliadas
        self.ramos = estado_inicial.vizinhos

    def custo_ramos(self):
        custo_ramos = []
        for ramo in self.ramos:
            custo_ramos.append(self.distancias + ramo.custo())

        return custo_ramos

    def adiciona(self, Ramo):
        self.distancias += Ramo.distancia
        self.estados.append(Ramo.node)
        self.ramos = Ramo.node.vizinhos

    def retira(self, Ramo):
        for ramo in self.ramos:
            if ramo.node.estado == Ramo.node.estado:
                self.ramos.remove(ramo)

    def __str__(self):
        estados = ""
        for node in self.estados:
            estados += " -> {}".format(node)
        return "{} - {}".format(estados, self.distancias)


class VetorOrdenado:
    def __init__(self, tamanho):
        self.numeroElementos = 0
        self.estados = [None] * tamanho

    def inserir(self, estado):
        if self.numeroElementos == 0:
            self.estados[0] = estado
            self.numeroElementos = 1
            return

        posicao = 0
        i = 0
        while i < self.numeroElementos:
            if estado.distancia > self.estados[posicao].distancia:
                posicao += 1
            i += 1

        for k in range(self.numeroElementos, posicao, -1):
            self.estados[k] = self.estados[k - 1]

        self.estados[posicao] = estado
        self.numeroElementos = self.numeroElementos + 1

    def getPrimeiro(self):
        return self.estados[0]

    def mostrar(self):
        for i in range(0, self.numeroElementos):
            print("{} - {}".format(self.estados[i].estado, self.estados[i].distancia))
