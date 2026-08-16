import time
import math
import tracemalloc
import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.dirname(__file__))

from Algoritmos.Backtracking import Backtracking
from Algoritmos.BranchAndBound import BranchAndBound
from Algoritmos.ProgramacaoDinamica import ProgramacaoDinamica
from Algoritmos.EstrategiaGulosa import EstrategiaGulosa
from Algoritmos.TwoOpt import TwoOpt
from Controller import relatorioController, graficoController
from IO import leitor_entrada, escritor_saida

def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def executar_teste():
    try:
        alg, n, pontos = leitor_entrada.ler_dados_teste()

        total = n + 1
        matriz = [[0.0] * total for _ in range(total)]
        for i in range(total):
            for j in range(total):
                matriz[i][j] = calcular_distancia(pontos[i], pontos[j])

        inicio = time.perf_counter()
        # mede memória alocada durante a execução do solver
        tracemalloc.start()

        if alg == "1":
            nome_alg = "Branch and Bound"
            solver = BranchAndBound(matriz)
        elif alg == "2":
            nome_alg = "Backtracking"
            solver = Backtracking(matriz)
        elif alg == "3":
            nome_alg = "Programação Dinâmica"
            solver = ProgramacaoDinamica(matriz)
        elif alg == "4":
            nome_alg = "Estratégia Gulosa"
            solver = EstrategiaGulosa(matriz)
        else:
            nome_alg = "2-Opt"
            solver = TwoOpt(matriz)
            
        melhor_distancia, melhor_rota, estados_explorados = solver.resolver()

        # memória em bytes (peak durante a iteração)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memoria_peak_kb = peak / 1024.0

        tempo = time.perf_counter() - inicio
        
        # Ajusta a rota para o formato de saída desejado
        rota_final = [p for p in melhor_rota if p != 0]


        escritor_saida.imprimir_resultado(melhor_distancia, rota_final)
        relatorioController.adicionar_relatorio({
            "algoritmo": nome_alg,
            "n": n,
            "distancia": melhor_distancia,
            "rota": "0 " + " ".join(map(str, rota_final)) + " 0",
            "tempo": tempo,
            "estados": estados_explorados,
            "memoria_peak": memoria_peak_kb,
            "chamadas_recursivas": getattr(solver, 'chamadas_recursivas', None),
            "podas": getattr(solver, 'podas', None),
            "profundidade_max": getattr(solver, 'profundidade_max', None),
            "status": "Sucesso"
        })

    except Exception as e:
        relatorioController.adicionar_relatorio({
            "algoritmo": "Indefinido",
            "n": None,
            "distancia": None,
            "rota": None,
            "tempo": 0.0,
            "estados": 0,
            "status": "Falhou",
            "erro": str(e)
        })
        escritor_saida.imprimir_mensagem(f"Erro no teste: {e}. Registrado no relatório.")

def main():
    while True:
        try:
            escritor_saida.imprimir_menu()
            op = leitor_entrada.ler_opcao_menu()

            if op == "0":
                escritor_saida.imprimir_mensagem("Encerrando aplicação...")
                break
            elif op == "1":
                executar_teste()
            elif op == "2":
                relatorioController.imprimir_relatorios()
            elif op == "3":
                nome = leitor_entrada.ler_nome_arquivo()
                relatorioController.salvar_relatorios_txt(nome)
            elif op == "4":
                graficoController.executar_testes_e_plotar()
            else:
                escritor_saida.imprimir_mensagem("Opção inválida.")

        except (EOFError, KeyboardInterrupt):
            escritor_saida.imprimir_mensagem("\nEntrada interrompida. Retornando ao menu...")
            continue

if __name__ == "__main__":
    main()