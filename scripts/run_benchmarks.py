import argparse
import sys
import os

# Adicionar src ao path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

from Controller import graficoController

parser = argparse.ArgumentParser(description='Run TSP benchmarks')
parser.add_argument('--min-n', type=int, default=3)
parser.add_argument('--max-n', type=int, default=9)
parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--save-instances', action='store_true')
parser.add_argument('--out-dir', type=str, default='Relatorios')
parser.add_argument('--skip-backtracking-above', type=int, default=9,
                    help='Skip running Backtracking for n greater than this value')

args = parser.parse_args()

ns = list(range(args.min_n, args.max_n + 1))

# graficoController already supports parameters; pass through
graficoController.executar_testes_e_plotar(ns=ns, seed=args.seed, save_instances=args.save_instances, out_dir=args.out_dir)
print('Benchmarks concluídos. Resultados em', args.out_dir)
