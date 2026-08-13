import random
import time
import tracemalloc
import os
import csv
import math
from Algoritmos.Backtracking import Backtracking
from Algoritmos.BranchAndBound import BranchAndBound
from Algoritmos.ProgramacaoDinamica import ProgramacaoDinamica
from Algoritmos.EstrategiaGulosa import EstrategiaGulosa
from Algoritmos.TwoOpt import TwoOpt

out_dir = os.path.join(os.path.dirname(__file__), '..', 'Relatorios')
os.makedirs(out_dir, exist_ok=True)

ns = list(range(3, 12))  # 3..11
seed = 42
random.seed(seed)

rows = []
for n in ns:
    print(f"Running n={n}")
    pontos = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n + 1)]
    matriz = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            matriz[i][j] = math.hypot(pontos[i][0] - pontos[j][0], pontos[i][1] - pontos[j][1])

    # Backtracking: skip when n > 8
    if n <= 8:
        bt = Backtracking(matriz)
        tracemalloc.start()
        t0 = time.perf_counter()
        dist_bt, rota_bt, estados_bt = bt.resolver()
        tempo_bt = time.perf_counter() - t0
        cur, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        mem_bt = peak / 1024.0
        chamadas_bt = getattr(bt, 'chamadas_recursivas', None)
        podas_bt = getattr(bt, 'podas', None)
        profund_bt = getattr(bt, 'profundidade_max', None)
    else:
        dist_bt = None
        tempo_bt = None
        estados_bt = None
        mem_bt = None
        chamadas_bt = None
        podas_bt = None
        profund_bt = None

    # Branch and Bound
    bb = BranchAndBound(matriz)
    tracemalloc.start()
    t0 = time.perf_counter()
    dist_bb, rota_bb, estados_bb = bb.resolver()
    tempo_bb = time.perf_counter() - t0
    cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_bb = peak / 1024.0
    chamadas_bb = getattr(bb, 'chamadas_recursivas', None)
    podas_bb = getattr(bb, 'podas', None)
    profund_bb = getattr(bb, 'profundidade_max', None)

    # Programacao Dinamica
    pd = ProgramacaoDinamica(matriz)
    tracemalloc.start()
    t0 = time.perf_counter()
    dist_pd, rota_pd, estados_pd = pd.resolver()
    tempo_pd = time.perf_counter() - t0
    cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_pd = peak / 1024.0
    chamadas_pd = getattr(pd, 'chamadas_recursivas', None)
    podas_pd = getattr(pd, 'podas', None)
    profund_pd = getattr(pd, 'profundidade_max', None)

    # Gulosa
    eg = EstrategiaGulosa(matriz)
    tracemalloc.start()
    t0 = time.perf_counter()
    dist_eg, rota_eg, estados_eg = eg.resolver()
    tempo_eg = time.perf_counter() - t0
    cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_eg = peak / 1024.0
    chamadas_eg = getattr(eg, 'chamadas_recursivas', None)
    podas_eg = getattr(eg, 'podas', None)
    profund_eg = getattr(eg, 'profundidade_max', None)

    # 2-Opt
    to = TwoOpt(matriz)
    tracemalloc.start()
    t0 = time.perf_counter()
    dist_to, rota_to, estados_to = to.resolver()
    tempo_to = time.perf_counter() - t0
    cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    mem_to = peak / 1024.0
    chamadas_to = getattr(to, 'chamadas_recursivas', None)
    podas_to = getattr(to, 'podas', None)
    profund_to = getattr(to, 'profundidade_max', None)

    # best exact
    exacts = [d for d in (dist_bt, dist_bb, dist_pd) if d is not None]
    best_exact = min(exacts) if exacts else None
    gap_eg = 100.0 * (dist_eg - best_exact) / best_exact if (best_exact and best_exact > 0) else None
    gap_to = 100.0 * (dist_to - best_exact) / best_exact if (best_exact and best_exact > 0) else None

    # append rows for CSV (one row per algorithm per n)
    def add_row(alg, dist, tempo, estados, mem, chamadas, podas, profund, gap):
        rows.append({
            'n': n,
            'algoritmo': alg,
            'tempo_s': '' if tempo is None else repr(tempo),
            'estados': '' if estados is None else estados,
            'memoria_kb': '' if mem is None else repr(mem),
            'chamadas_recursivas': '' if chamadas is None else chamadas,
            'podas': '' if podas is None else podas,
            'profundidade_max': '' if profund is None else profund,
            'gap_percent': '' if gap is None else ('{:.6f}'.format(gap)),
        })

    add_row('Backtracking', dist_bt, tempo_bt, estados_bt, mem_bt, chamadas_bt, podas_bt, profund_bt, None)
    add_row('BranchAndBound', dist_bb, tempo_bb, estados_bb, mem_bb, chamadas_bb, podas_bb, profund_bb, None)
    add_row('ProgramacaoDinamica', dist_pd, tempo_pd, estados_pd, mem_pd, chamadas_pd, podas_pd, profund_pd, None)
    add_row('Gulosa', dist_eg, tempo_eg, estados_eg, mem_eg, chamadas_eg, podas_eg, profund_eg, gap_eg)
    add_row('TwoOpt', dist_to, tempo_to, estados_to, mem_to, chamadas_to, podas_to, profund_to, gap_to)

# save CSV
csv_path = os.path.join(out_dir, 'benchmark_metrics.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['n','algoritmo','tempo_s','estados','memoria_kb','chamadas_recursivas','podas','profundidade_max','gap_percent'])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print('Saved CSV to', csv_path)

# now create some summary plots (reuse simple plotting)
import matplotlib.pyplot as plt
from collections import defaultdict

# read back CSV
data = defaultdict(lambda: defaultdict(list))
with open(csv_path, encoding='utf-8') as f:
    import csv as _csv
    rd = _csv.DictReader(f)
    for r in rd:
        n = int(r['n'])
        alg = r['algoritmo']
        def tof(x):
            try:
                return float(x)
            except:
                return None
        data[alg]['n'].append(n)
        data[alg]['tempo'].append(tof(r['tempo_s']))
        data[alg]['estados'].append(tof(r['estados']))
        data[alg]['memoria'].append(tof(r['memoria_kb']))
        data[alg]['gap'].append(tof(r['gap_percent']))

# time plot
plt.figure(figsize=(10,6))
for alg, vals in data.items():
    if any(v is not None for v in vals['tempo']):
        plt.plot(vals['n'], [v if v is not None else float('nan') for v in vals['tempo']], marker='o', label=alg)
plt.title('Tempo de Execução vs Nº de Clientes')
plt.xlabel('Nº de Clientes')
plt.ylabel('Tempo (s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(out_dir,'grafico_tempo_estendido.png'), dpi=150, bbox_inches='tight')
print('Saved', os.path.join(out_dir,'grafico_tempo_estendido.png'))
plt.close()

# memory plot
plt.figure(figsize=(10,6))
for alg, vals in data.items():
    if any(v is not None for v in vals['memoria']):
        plt.plot(vals['n'], [v if v is not None else float('nan') for v in vals['memoria']], marker='o', label=alg)
plt.title('Memória peak (KB) vs Nº de Clientes')
plt.xlabel('Nº de Clientes')
plt.ylabel('Memória (KB)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(out_dir,'grafico_memoria_estendido.png'), dpi=150, bbox_inches='tight')
print('Saved', os.path.join(out_dir,'grafico_memoria_estendido.png'))
plt.close()

# gap plot
plt.figure(figsize=(10,6))
plotted=False
for alg in ('Gulosa','TwoOpt'):
    vals=data.get(alg)
    if vals and any(v is not None for v in vals['gap']):
        plt.plot(vals['n'], [v if v is not None else float('nan') for v in vals['gap']], marker='o', label=alg)
        plotted=True
if plotted:
    plt.title('GAP% heurísticas vs best exact')
    plt.xlabel('Nº de Clientes')
    plt.ylabel('GAP (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir,'grafico_gap_estendido.png'), dpi=150, bbox_inches='tight')
    print('Saved', os.path.join(out_dir,'grafico_gap_estendido.png'))
    plt.close()

print('Extended benchmark complete. Results in', out_dir)
