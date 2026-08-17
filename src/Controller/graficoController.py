import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time
import random
import os
import tracemalloc
import csv
from Algoritmos.Backtracking import Backtracking
from Algoritmos.BranchAndBound import BranchAndBound
from Algoritmos.ProgramacaoDinamica import ProgramacaoDinamica
from Algoritmos.EstrategiaGulosa import EstrategiaGulosa

def calcular_distancia(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def executar_testes_e_plotar(ns=None, seed=42, save_instances=False, out_dir="Relatorios"):
    if ns is None:
        ns = list(range(3, 11))
    tempos_bt = []
    tempos_bb = []
    tempos_pd = []
    tempos_eg = []
    estados_bt = []
    estados_bb = []
    estados_pd = []
    estados_eg = []
    # métricas adicionais
    mem_bt = []
    mem_bb = []
    mem_pd = []
    mem_eg = []

    chamadas_bt = []
    chamadas_bb = []
    chamadas_pd = []
    chamadas_eg = []

    podas_bt = []
    podas_bb = []
    podas_pd = []
    podas_eg = []

    profund_bt = []
    profund_bb = []
    profund_pd = []
    profund_eg = []

    # listas para 2-opt e gaps
    tempos_to = []
    estados_to = []
    mem_to = []
    chamadas_to = []
    podas_to = []
    profund_to = []
    distancias_bt = []
    distancias_bb = []
    distancias_pd = []
    distancias_eg = []
    distancias_to = []
    gap_eg = []
    gap_to = []

    random.seed(seed)

    for n in ns:
        print(f"Testando com n = {n}...")
        pontos = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n + 1)]
        matriz_dist = [[calcular_distancia(pontos[i], pontos[j]) for j in range(n + 1)] for i in range(n + 1)]

        if save_instances:
            os.makedirs(out_dir, exist_ok=True)
            inst_path = os.path.join(out_dir, f"instance_n{n}.txt")
            with open(inst_path, "w", encoding='utf-8') as f:
                f.write(str(n) + "\n")
                for x, y in pontos:
                    f.write(f"{x} {y}\n")

        # Backtracking
        bt = Backtracking(matriz_dist)
        tracemalloc.start()
        inicio = time.perf_counter()
        dist_bt, rota_bt, estados = bt.resolver()
        tempo_bt = time.perf_counter() - inicio
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tempos_bt.append(tempo_bt)
        estados_bt.append(estados)
        mem_bt.append(peak / 1024.0)
        chamadas_bt.append(getattr(bt, 'chamadas_recursivas', None))
        podas_bt.append(getattr(bt, 'podas', None))
        profund_bt.append(getattr(bt, 'profundidade_max', None))
        distancias_bt.append(dist_bt)

        # Branch and Bound
        bb = BranchAndBound(matriz_dist)
        tracemalloc.start()
        inicio = time.perf_counter()
        dist_bb, rota_bb, estados = bb.resolver()
        tempo_bb = time.perf_counter() - inicio
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tempos_bb.append(tempo_bb)
        estados_bb.append(estados)
        mem_bb.append(peak / 1024.0)
        chamadas_bb.append(getattr(bb, 'chamadas_recursivas', None))
        podas_bb.append(getattr(bb, 'podas', None))
        profund_bb.append(getattr(bb, 'profundidade_max', None))
        distancias_bb.append(dist_bb)

        # Programacao Dinamica
        pd = ProgramacaoDinamica(matriz_dist)
        tracemalloc.start()
        inicio = time.perf_counter()
        dist_pd, rota_pd, estados = pd.resolver()
        tempo_pd = time.perf_counter() - inicio
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tempos_pd.append(tempo_pd)
        estados_pd.append(estados)
        mem_pd.append(peak / 1024.0)
        chamadas_pd.append(getattr(pd, 'chamadas_recursivas', None))
        podas_pd.append(getattr(pd, 'podas', None))
        profund_pd.append(getattr(pd, 'profundidade_max', None))
        distancias_pd.append(dist_pd)

        # Estrategia Gulosa
        eg = EstrategiaGulosa(matriz_dist)
        tracemalloc.start()
        inicio = time.perf_counter()
        dist_eg, rota_eg, estados = eg.resolver()
        tempo_eg = time.perf_counter() - inicio
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tempos_eg.append(tempo_eg)
        estados_eg.append(estados)
        mem_eg.append(peak / 1024.0)
        chamadas_eg.append(getattr(eg, 'chamadas_recursivas', None))
        podas_eg.append(getattr(eg, 'podas', None))
        profund_eg.append(getattr(eg, 'profundidade_max', None))
        distancias_eg.append(dist_eg)

        # 2-Opt
        from Algoritmos.TwoOpt import TwoOpt
        to = TwoOpt(matriz_dist)
        tracemalloc.start()
        inicio = time.perf_counter()
        dist_to, rota_to, estados = to.resolver()
        tempo_to = time.perf_counter() - inicio
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tempos_to.append(tempo_to)
        estados_to.append(estados)
        mem_to.append(peak / 1024.0)
        chamadas_to.append(getattr(to, 'chamadas_recursivas', None))
        podas_to.append(getattr(to, 'podas', None))
        profund_to.append(getattr(to, 'profundidade_max', None))
        distancias_to.append(dist_to)

        # Gaps em relação ao melhor exato disponível
        exacts = [d for d in (dist_bt, dist_bb, dist_pd) if d is not None]
        best_exact = min(exacts) if exacts else None
        gap_eg.append(100.0 * (dist_eg - best_exact) / best_exact if best_exact and best_exact > 0 else None)
        gap_to.append(100.0 * (dist_to - best_exact) / best_exact if best_exact and best_exact > 0 else None)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.plot(ns, tempos_bt, label='Backtracking', marker='o', color='red')
    ax1.plot(ns, tempos_bb, label='Branch and Bound', marker='s', color='blue')
    ax1.plot(ns, tempos_pd, label='Programação Dinâmica', marker='^', color='green')
    ax1.plot(ns, tempos_eg, label='Gulosa', marker='d', color='orange')
    ax1.set_title('Tempo de Execução vs Número de Clientes')
    ax1.set_xlabel('Nº de Clientes')
    ax1.set_ylabel('Tempo (segundos)')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(ns, estados_bt, label='Backtracking', marker='o', color='red')
    ax2.plot(ns, estados_bb, label='Branch and Bound', marker='s', color='blue')
    ax2.plot(ns, estados_pd, label='Programação Dinâmica', marker='^', color='green')
    ax2.plot(ns, estados_eg, label='Gulosa', marker='d', color='orange')
    ax2.set_title('Estados Explorados (Nós da Árvore/Passos)')
    ax2.set_xlabel('Nº de Clientes')
    ax2.set_ylabel('Quantidade de Estados')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    os.makedirs("Relatorios", exist_ok=True)
    plt.savefig("Relatorios/grafico_comparativo.png", dpi=150, bbox_inches='tight')
    print("\nGráfico salvo em 'Relatorios/grafico_comparativo.png'")
    # Gráfico de memória
    plt.figure(figsize=(10,6))
    if mem_bt:
        plt.plot(ns, mem_bt, marker='o', label='Backtracking')
    if mem_bb:
        plt.plot(ns, mem_bb, marker='s', label='Branch and Bound')
    if mem_pd:
        plt.plot(ns, mem_pd, marker='^', label='Programação Dinâmica')
    if mem_eg:
        plt.plot(ns, mem_eg, marker='d', label='Gulosa')
    if mem_to:
        plt.plot(ns, mem_to, marker='x', label='2-Opt')
    plt.title('Memória peak (KB) vs Nº de Clientes')
    plt.xlabel('Nº de Clientes')
    plt.ylabel('Memória (KB)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Relatorios/grafico_memoria_comparativo.png', dpi=150, bbox_inches='tight')
    print("Gráfico de memória salvo em 'Relatorios/grafico_memoria_comparativo.png'")

    # Gráfico de GAP para heurísticas
    plt.figure(figsize=(10,6))
    if any(g is not None for g in gap_eg):
        plt.plot(ns, [g if g is not None else float('nan') for g in gap_eg], marker='d', label='Gulosa GAP%')
    if any(g is not None for g in gap_to):
        plt.plot(ns, [g if g is not None else float('nan') for g in gap_to], marker='x', label='2-Opt GAP%')
    plt.title('GAP% das heurísticas vs melhor exato')
    plt.xlabel('Nº de Clientes')
    plt.ylabel('GAP (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Relatorios/grafico_gap_comparativo.png', dpi=150, bbox_inches='tight')
    print("Gráfico de GAP salvo em 'Relatorios/grafico_gap_comparativo.png'")
    # salva CSV com métricas detalhadas
    csv_path = os.path.join("Relatorios", "benchmark_metrics.csv")
    with open(csv_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["n", "algoritmo", "tempo_s", "estados", "memoria_kb", "chamadas_recursivas", "podas", "profundidade_max", "gap_percent"])
        for i, n in enumerate(ns):
            writer.writerow([n, 'Backtracking', tempos_bt[i], estados_bt[i], mem_bt[i], chamadas_bt[i], podas_bt[i], profund_bt[i], ''])
            writer.writerow([n, 'BranchAndBound', tempos_bb[i], estados_bb[i], mem_bb[i], chamadas_bb[i], podas_bb[i], profund_bb[i], ''])
            writer.writerow([n, 'ProgramacaoDinamica', tempos_pd[i], estados_pd[i], mem_pd[i], chamadas_pd[i], podas_pd[i], profund_pd[i], ''])
            writer.writerow([n, 'Gulosa', tempos_eg[i], estados_eg[i], mem_eg[i], chamadas_eg[i], podas_eg[i], profund_eg[i], f"{gap_eg[i]:.6f}" if gap_eg[i] is not None else ''])
            writer.writerow([n, 'TwoOpt', tempos_to[i], estados_to[i], mem_to[i], chamadas_to[i], podas_to[i], profund_to[i], f"{gap_to[i]:.6f}" if gap_to[i] is not None else ''])

    print(f"\nMétricas salvas em '{csv_path}'")
    plt.show()
