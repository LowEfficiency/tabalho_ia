import os
import statistics
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.TSP import TSP
from src.WOA import WOA

class ExperimentoWOA:
    def __init__(self, caminho_instancia, n_execucoes=20, n_geracoes=200, pasta_base="resultados"):
        self.tsp = TSP(caminho_instancia)
        self.n_execucoes = n_execucoes
        self.n_geracoes = n_geracoes
        
        self.pasta_saida = self._configurar_pasta_saida(caminho_instancia, pasta_base)
        self.populacoes = [50, 100]
        
        self.dados_tabela = [] 
        self.dados_brutos_boxplot = []
        self.convergencia_global = {}

    def _configurar_pasta_saida(self, caminho_instancia, pasta_base):
        nome_instancia = os.path.splitext(os.path.basename(caminho_instancia))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pasta_saida = os.path.join(pasta_base, "WOA", f"{nome_instancia}_{timestamp}")
        os.makedirs(pasta_saida, exist_ok=True)
        return pasta_saida

    def rodar(self):
        print(f"\nIniciando Experimento WOA")
        for idx, pop in enumerate(self.populacoes, start=1):
            id_config = f"WOA_P{pop}"
            print(f"Executando {id_config}: Pop={pop}")
            
            matriz_convergencia = np.zeros((self.n_execucoes, self.n_geracoes))
            fitness_execucoes = []
            melhor_rota_global = None
            melhor_fitness_global = float('inf')
            
            for rodada in range(self.n_execucoes):
                woa = WOA(
                    tamanho_pop=pop,
                    n_geracoes=self.n_geracoes,
                    tsp_instancia=self.tsp
                )
                
                for gen in range(self.n_geracoes):
                    woa.evolucao()
                    matriz_convergencia[rodada, gen] = woa.melhor_individuo.fitness
                
                fitness_final = woa.melhor_individuo.fitness
                fitness_execucoes.append(fitness_final)
                
                if fitness_final < melhor_fitness_global:
                    melhor_fitness_global = fitness_final
                    melhor_rota_global = woa.melhor_individuo.rota[:]
                
                self.dados_brutos_boxplot.append({
                    'Config': id_config,
                    'Fitness': fitness_final
                })
                
            self.convergencia_global[id_config] = np.mean(matriz_convergencia, axis=0)
            
            self.dados_tabela.append({
                'ID': id_config,
                'Pop': pop,
                'Melhor': min(fitness_execucoes),
                'Pior': max(fitness_execucoes),
                'Média': statistics.mean(fitness_execucoes),
                'Mediana': statistics.median(fitness_execucoes),
                'Desvio Padrão': statistics.stdev(fitness_execucoes),
                'Vetor Melhor Rota': str(melhor_rota_global)
            })

    def exportar_resultados(self):
        df_tabela = pd.DataFrame(self.dados_tabela)
        df_tabela.to_csv(os.path.join(self.pasta_saida, "metricas_woa.csv"), index=False, sep=';')
        
        df_box = pd.DataFrame(self.dados_brutos_boxplot)
        sns.set_theme(style="whitegrid")
        
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Config', y='Fitness', data=df_box, hue='Config', palette="Set2", legend=False)
        plt.title("Boxplot - Experimento WOA")
        plt.tight_layout()
        plt.savefig(os.path.join(self.pasta_saida, "boxplot_woa.png"))
        plt.close()

        plt.figure(figsize=(10, 6))
        for id_config, valores in self.convergencia_global.items():
            plt.plot(valores, label=id_config, linewidth=2)
        plt.title("Convergência Média - Experimento WOA")
        plt.xlabel("Gerações")
        plt.ylabel("Fitness")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.pasta_saida, "convergencia_woa.png"))
        plt.close()
        print(f"Resultados WOA salvos em: {self.pasta_saida}")