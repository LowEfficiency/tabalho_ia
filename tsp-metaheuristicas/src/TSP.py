import math

class TSP:
    def __init__(self, caminho):
        self.matriz_distancia = self._carregar_matriz(caminho)

    def calcular_distancia(self, pontoa, pontob):
        return self.matriz_distancia[pontoa][pontob]

    def _dist_coords(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def _carregar_matriz(self, caminho):
        try:
            with open(caminho, 'r') as arquivo:
                linhas = arquivo.readlines()

            # remove linhas vazias
            linhas = [linha.strip() for linha in linhas if linha.strip()]

            # primeira linha = quantidade de cidades
            n = int(linhas[0])

            coordenadas = []

            # lê coordenadas
            for linha in linhas[1:n+1]:
                x, y = map(float, linha.split())
                coordenadas.append((x, y))

            # cria matriz de distâncias
            matriz = []

            for i in range(n):
                linha_distancias = []

                for j in range(n):
                    distancia = self._dist_coords(
                        coordenadas[i],
                        coordenadas[j]
                    )

                    linha_distancias.append(distancia)

                matriz.append(linha_distancias)

            return matriz

        except FileNotFoundError:
            print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
            return []

    def exibir_matriz(self):
        for linha in self.matriz_distancia:
            print(linha)

    def get_n_cidades(self):
        return len(self.matriz_distancia)