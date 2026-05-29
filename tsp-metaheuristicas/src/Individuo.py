
from src.TSP import TSP

class Individuo:
    def __init__(self, rota, tsp):
        self.rota = rota
        self.fitness = self.calculo_fitness(tsp)
        
    def calculo_fitness(self, tsp) -> float:
        distancia_total = 0
        n = len(self.rota)
        
        for i in range (n - 1):
            cidade_atual = self.rota[i]
            proxima_cidade = self.rota[i + 1]
            distancia_total += tsp.calcular_distancia(cidade_atual, proxima_cidade)
        
        cidade_inicial = self.rota[0]
        cidade_final = self.rota[-1]
        distancia_total += tsp.calcular_distancia(cidade_inicial, cidade_final)
        
        return distancia_total
    
        