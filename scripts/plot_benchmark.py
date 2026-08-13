import csv
import matplotlib.pyplot as plt
import os
from collections import defaultdict

csv_path = os.path.join('Relatorios', 'benchmark_metrics.csv')
if not os.path.exists(csv_path):
    print('CSV de benchmark não encontrado:', csv_path)
    raise SystemExit(1)

# read CSV
rows = []
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

# organize data by algorithm
data = defaultdict(lambda: defaultdict(list))
ns = []
for r in rows:
    n = int(r['n'])
    alg = r['algoritmo']
    if n not in ns:
        ns.append(n)
    # safe conversions
    def to_float(x):
        try:
            return float(x)
        except:
            return None
    data[alg]['n'].append(n)
    data[alg]['tempo'].append(to_float(r.get('tempo_s', '')))
    data[alg]['estados'].append(to_float(r.get('estados', '')))
    data[alg]['memoria'].append(to_float(r.get('memoria_kb', '')))
    gap = r.get('gap_percent', '')
    data[alg]['gap'].append(to_float(gap) if gap != '' else None)

ns = sorted(list(set(ns)))

# Plot time
plt.figure(figsize=(10,6))
for alg, vals in data.items():
    if vals['tempo']:
        plt.plot(vals['n'], vals['tempo'], marker='o', label=alg)
plt.title('Tempo de Execução vs Nº de Clientes')
plt.xlabel('Nº de Clientes')
plt.ylabel('Tempo (s)')
plt.legend()
plt.grid(True)
plt.tight_layout()
os.makedirs('Relatorios', exist_ok=True)
plt.savefig(os.path.join('Relatorios','grafico_tempo_detalhado.png'), dpi=150)
print('Salvo Relatorios/grafico_tempo_detalhado.png')
plt.close()

# Plot states (log)
plt.figure(figsize=(10,6))
for alg, vals in data.items():
    if vals['estados']:
        plt.plot(vals['n'], vals['estados'], marker='o', label=alg)
plt.yscale('log')
plt.title('Estados Explorados vs Nº de Clientes (escala log)')
plt.xlabel('Nº de Clientes')
plt.ylabel('Estados (log)')
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.savefig(os.path.join('Relatorios','grafico_estados_detalhado.png'), dpi=150)
print('Salvo Relatorios/grafico_estados_detalhado.png')
plt.close()

# Plot memory
plt.figure(figsize=(10,6))
for alg, vals in data.items():
    if vals['memoria']:
        plt.plot(vals['n'], vals['memoria'], marker='o', label=alg)
plt.title('Memória peak (KB) vs Nº de Clientes')
plt.xlabel('Nº de Clientes')
plt.ylabel('Memória (KB)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join('Relatorios','grafico_memoria_detalhado.png'), dpi=150)
print('Salvo Relatorios/grafico_memoria_detalhado.png')
plt.close()

# Plot GAP for heuristics (if present)
plt.figure(figsize=(10,6))
plotted = False
for alg in data:
    if alg.lower() in ('gulosa', 'twoopt') and any(g is not None for g in data[alg]['gap']):
        plt.plot(data[alg]['n'], [g if g is not None else float('nan') for g in data[alg]['gap']], marker='o', label=alg)
        plotted = True
if plotted:
    plt.title('GAP% (heurísticas vs melhor exato)')
    plt.xlabel('Nº de Clientes')
    plt.ylabel('GAP (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join('Relatorios','grafico_gap_detalhado.png'), dpi=150)
    print('Salvo Relatorios/grafico_gap_detalhado.png')
    plt.close()
else:
    print('Nenhuma GAP disponível para plotagem.')

print('Plotagem concluída.')
