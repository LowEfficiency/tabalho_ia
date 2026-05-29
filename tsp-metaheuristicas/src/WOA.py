import numpy as np
import random
import math
from src.Individuo import Individuo

class WOA:
    def __init__(self, tamanho_pop, n_geracoes, tsp_instancia):
        self.tamanho_pop = tamanho_pop
        self.n_geracoes = n_geracoes
        self.tsp = tsp_instancia
        self.n_dimensoes = tsp_instancia.get_n_cidades()
        
        # O WOA original tem um contador interno para reduzir o cerco
        self.geracao_atual = 0

        # Limites do espaço contínuo onde as baleias vão nadar
        # O tamanho exato não importa tanto, contanto que seja simétrico
        self.limite_inferior = -10.0
        self.limite_superior = 10.0

        # Guarda a melhor presa
        self.melhor_posicao_continua = None
        self.melhor_individuo = None
        
        # População contínua
        self.populacao_continua = self._iniciar_populacao_continua()

        # População discreta
        self.populacao = []

        # Faz a primeira avaliação para definir a Presa inicial
        self._avaliar_populacao()
    
    def _iniciar_populacao_continua(self):
        return np.random.uniform(
            self.limite_inferior,
            self.limite_superior,
            (self.tamanho_pop, self.n_dimensoes)
        )
        
    def _spv(self, vetor_continuo):
        #retorna a lista de posicoes em ordem crescente
        return np.argsort(vetor_continuo).tolist()
    
    def _avaliar_populacao(self):
       self.populacao = []
       
       for i in range(self.tamanho_pop):
           posicao_continua = self.populacao_continua[i]
           
           rota_discreta = self._spv(posicao_continua)
           
           individuo = Individuo(rota_discreta, self.tsp)
           self.populacao.append(individuo)
           
           if self.melhor_individuo is None or individuo.fitness < self.melhor_individuo.fitness:
               self.melhor_individuo = individuo
               self.melhor_posicao_continua = np.copy(posicao_continua)
               
    def evolucao(self):
        self.geracao_atual += 1
        
        a = 2.0 - self.geracao_atual * (2.0 / self.n_geracoes)
        
        for i in range(self.tamanho_pop):
            r1 = random.random()
            r2 = random.random()
            
            A = 2.0 * a * r1 - a
            C = 2.0 * r2
            b = 1.0
            l = random.uniform(-1, 1)
            p = random.random()
            
            posicao_atual = self.populacao_continua[i]
            
            if p < 0.5:
                if abs(A) < 1:
                    # 1. Fase de Explotação: Cerco à Presa
                    D = np.abs(C * self.melhor_posicao_continua - posicao_atual)
                    nova_posicao = self.melhor_posicao_continua - A * D
                else:
                    # 2. Fase de Exploração: Busca por Presa
                    idx_rand = random.randint(0, self.tamanho_pop - 1)
                    posicao_rand = self.populacao_continua[idx_rand]
                    
                    D = np.abs(C * posicao_rand - posicao_atual)
                    nova_posicao = posicao_rand - A * D
                    
            else:
                # 3. Ataque em Rede de Bolhas: Movimento em Espiral
                D_linha = np.abs(self.melhor_posicao_continua - posicao_atual)
                nova_posicao = D_linha * math.exp(b * l) * math.cos(2 * math.pi * l) + self.melhor_posicao_continua
            
            nova_posicao = np.clip(nova_posicao, self.limite_inferior, self.limite_superior)
            
            self.populacao_continua[i] = nova_posicao
            
        self._avaliar_populacao()
                