import os
import statistics
from datetime import datetime
from itertools import product
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.TSP import TSP
from src.AG import AG

class ExperimentoAG:
    def __init__(self, caminho_instancia, n_execucoes=20, n_geracoes=200, pasta_base="resultados"):
        self.tsp = TSP(caminho_instancia)
        self.n_execucoes = n_execucoes
        self.n_geracoes = n_geracoes
        
        self.pasta_saida = self._configurar_pasta_saida(caminho_instancia, pasta_base)
       
        self.fatores = {
            'populacao': [50, 100],
            'taxa_cruzamento': [0.8, 0.9],
            'taxa_mutacao': [0.01, 0.05],
            'operador': ['OX', 'PMX']
        }
        
        self.dados_tabela = [] 
        self.dados_brutos_boxplot = []
        self.convergencia_global = {}

    def _configurar_pasta_saida(self, caminho_instancia, pasta_base):
        nome_instancia = os.path.splitext(os.path.basename(caminho_instancia))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pasta_saida = os.path.join(pasta_base, "AG", f"{nome_instancia}_{timestamp}")
        os.makedirs(pasta_saida, exist_ok=True)
        return pasta_saida

    def rodar(self):
        print(f"\nIniciando Experimento AG")
        chaves, valores = zip(*self.fatores.items())
        combinacoes = [dict(zip(chaves, v)) for v in product(*valores)]
        
        for idx, config in enumerate(combinacoes, 1):
            id_config = f"AG_C{idx}"
            print(f"Executando {id_config}: Pop={config['populacao']} | Cr={config['taxa_cruzamento']} | Mt={config['taxa_mutacao']} | Op={config['operador']}")
            
            matriz_convergencia = np.zeros((self.n_execucoes, self.n_geracoes))
            fitness_execucoes = []
            melhor_rota_global = None
            melhor_fitness_global = float('inf')
            
            for rodada in range(self.n_execucoes):
                ag = AG(
                    tamanho_pop=config['populacao'],
                    taxa_cruzamento=config['taxa_cruzamento'],
                    taxa_mutacao=config['taxa_mutacao'],
                    operador=config['operador'],
                    tsp_instancia=self.tsp
                )
                
                for gen in range(self.n_geracoes):
                    ag.evolucao()
                    melhor_ind = min(ag.populacao, key=lambda ind: ind.fitness)
                    matriz_convergencia[rodada, gen] = melhor_ind.fitness
                
                melhor_final = min(ag.populacao, key=lambda ind: ind.fitness)
                fitness_execucoes.append(melhor_final.fitness)
                
                if melhor_final.fitness < melhor_fitness_global:
                    melhor_fitness_global = melhor_final.fitness
                    melhor_rota_global = melhor_final.rota[:]
                
                self.dados_brutos_boxplot.append({
                    'Config': id_config,
                    'Fitness': melhor_final.fitness,
                    'Operador': config['operador']
                })
            
            self.convergencia_global[id_config] = np.mean(matriz_convergencia, axis=0)
            
            self.dados_tabela.append({
                'ID': id_config,
                'Pop': config['populacao'],
                'Cr': config['taxa_cruzamento'],
                'Mt': config['taxa_mutacao'],
                'Op': config['operador'],
                'Melhor': min(fitness_execucoes),
                'Pior': max(fitness_execucoes),
                'Média': statistics.mean(fitness_execucoes),
                'Mediana': statistics.median(fitness_execucoes),
                'Desvio Padrão': statistics.stdev(fitness_execucoes),
                'Vetor Melhor Rota': str(melhor_rota_global)
            })

    def exportar_resultados(self):
        df_tabela = pd.DataFrame(self.dados_tabela)
        df_tabela.to_csv(os.path.join(self.pasta_saida, "metricas_ag.csv"), index=False, sep=';')
        
        df_box = pd.DataFrame(self.dados_brutos_boxplot)
        sns.set_theme(style="whitegrid")
        
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Config', y='Fitness', hue='Operador', data=df_box)
        plt.title("Boxplot - Experimento AG")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.pasta_saida, "boxplot_ag.png"))
        plt.close()

        plt.figure(figsize=(12, 6))
        for id_config, valores in self.convergencia_global.items():
            plt.plot(valores, label=id_config)
        plt.title("Convergência Média - Experimento AG")
        plt.xlabel("Gerações")
        plt.ylabel("Fitness")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(self.pasta_saida, "convergencia_ag.png"))
        plt.close()
        print(f"Resultados AG salvos em: {self.pasta_saida}") 