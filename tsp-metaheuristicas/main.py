import os
from src.ExperimentoAG import ExperimentoAG
from src.ExperimentoWOA import ExperimentoWOA

def main():
    
    caminho_instancia = os.path.join("dados", "coordenadas.txt")
    EXECUCOES = 20
    GERACOES = 200
    
    print("=" * 80)
    print("METAHEURÍSTICAS PARA O TSP - AG & WOA")
    print(f"Instância: {caminho_instancia}")
    print("=" * 80)

    exp_ag = ExperimentoAG(caminho_instancia, n_execucoes=EXECUCOES, n_geracoes=GERACOES)
    exp_ag.rodar()
    exp_ag.exportar_resultados()
    
    exp_woa = ExperimentoWOA(caminho_instancia, n_execucoes=EXECUCOES, n_geracoes=GERACOES)
    exp_woa.rodar()
    exp_woa.exportar_resultados()
    
    print("\n" + "=" * 80)
    print("Os resultados foram separados dentro da pasta 'resultados/AG' e 'resultados/WOA'.")
    print("=" * 80)

if __name__ == "__main__":
    main()
