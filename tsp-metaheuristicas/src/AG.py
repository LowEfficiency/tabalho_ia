from src.Individuo import Individuo
from src.TSP import TSP
import random

class AG:
    
    def __init__(self, tamanho_pop, taxa_cruzamento, taxa_mutacao, operador, tsp_instancia):
        self.tamanho_pop = tamanho_pop
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.operador = operador
        self.tsp = tsp_instancia
        
        self.populacao = self.iniciar_populacao()
    
    def torneio(self, k=3):
        competidores = random.sample(self.populacao, k)
        vencedor = min(competidores, key=lambda ind: ind.fitness)
        
        return vencedor
    
    def sorteia_corte(self, tamanho_rota):
        pontos = random.sample(range(tamanho_rota), 2)
        pontos.sort()
        return pontos[0], pontos[1]
        
    def OX(self, pai1, pai2, tamanho_rota):
        pai1 = pai1.rota
        pai2 = pai2.rota
        
        inicio, fim = self.sorteia_corte(tamanho_rota)
        filho = [-1] * tamanho_rota #cria o vetor filho
        
        filho[inicio:fim + 1] = pai1[inicio:fim + 1] #faz a copia do segmento sorteado
        segmento_herdado = set(filho[inicio:fim + 1])
        
        posicao_filho = (fim + 1) % tamanho_rota #implementa a logica circular
        posicao_pai2 = (fim + 1) % tamanho_rota

        while -1 in filho:
            cidade = pai2[posicao_pai2] #salva em cidade  a cidade do indice que esta no pa12
            
            if cidade not in segmento_herdado: #verifica se nao e repetido
                filho[posicao_filho] = cidade
                posicao_filho = (posicao_filho + 1) % tamanho_rota #avança o indice
            
            posicao_pai2 = (posicao_pai2 + 1) % tamanho_rota #avança sempre para testar novos indices
        
        return Individuo(filho, self.tsp)
    
    def PMX(self, pai1_obj, pai2_obj, tamanho_rota):
        pai1, pai2 = pai1_obj.rota, pai2_obj.rota
        filho = [-1] * tamanho_rota
        
        inicio, fim = self.sorteia_corte(tamanho_rota)
        
        filho[inicio:fim + 1] = pai1[inicio:fim + 1]
        segmento_set = set(filho[inicio:fim+1])
        
        mapping = {}
        for k in range(inicio, fim + 1):
            mapping[pai1[k]] = pai2[k]  #mapeia as cidades usando p1 como chave e p2 como valor

        for i in range(tamanho_rota):
            if i < inicio or i > fim:
                cidade = pai2[i]
                while cidade in segmento_set: #roda o set para verificar se nao esta repetido
                    cidade = mapping[cidade] #mapeia as repetidas
                
                filho[i] = cidade
        
        return Individuo(filho, self.tsp)
    
    def mutacao(self, individuo):
        rota = individuo.rota
        tamanho = len(rota)
        
        for i in range(tamanho):
            r = random.random()
            if r <= self.taxa_mutacao:
                j = random.randint(0, tamanho - 1)
                rota[i], rota[j] = rota[j], rota[i]
                
        individuo.rota = rota
        individuo.fitness = individuo.calculo_fitness(self.tsp)
       
    def iniciar_populacao(self):
        pop = []
        
        n_cidades = self.tsp.get_n_cidades()
        cidades = list(range(n_cidades))
        
        for _ in range(self.tamanho_pop):
            rota = random.sample(cidades, n_cidades)
            pop.append(Individuo(rota, self.tsp))
        
        return pop

    def evolucao(self):
        nova_geracao = []
        
        melhor_atual = min(self.populacao, key=lambda ind: ind.fitness)
        nova_geracao.append(Individuo(melhor_atual.rota[:], self.tsp))
        
        while len(nova_geracao) < self.tamanho_pop:
            pai1 = self.torneio()
            pai2 = self.torneio()
            
            if random.random() <= self.taxa_cruzamento:
                if self.operador == "OX":
                    filho = self.OX(pai1, pai2, len(pai1.rota))
                elif self.operador == "PMX":
                    filho = self.PMX(pai1, pai2, len(pai1.rota))
                else:
                    return 0
            else:
                filho = Individuo(pai1.rota[:], self.tsp)
                
            self.mutacao(filho)
            nova_geracao.append(filho)
        
        self.populacao = nova_geracao