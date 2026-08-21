import time
import math
import tracemalloc
import sys
import os
import click
import questionary

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

def executar_teste_direto(alg, n, pontos):
    try:
        total = n + 1
        matriz = [[0.0] * total for _ in range(total)]
        for i in range(total):
            for j in range(total):
                matriz[i][j] = calcular_distancia(pontos[i], pontos[j])

        inicio = time.perf_counter()
        # mede memória alocada durante a execução do solver
        tracemalloc.start()

        # Mapeamento ajustado para o novo menu (opções em string)
        if alg == "Branch and Bound":
            nome_alg = "Branch and Bound"
            solver = BranchAndBound(matriz)
        elif alg == "Backtracking":
            nome_alg = "Backtracking"
            solver = Backtracking(matriz)
        elif alg == "Programação Dinâmica":
            nome_alg = "Programação Dinâmica"
            solver = ProgramacaoDinamica(matriz)
        elif alg == "Estratégia Gulosa":
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

def executar_teste():
    try:
        alg_map = {
            "Branch and Bound": "1",
            "Backtracking": "2",
            "Programação Dinâmica": "3",
            "Estratégia Gulosa": "4",
            "2-Opt (heurística de melhoria)": "5"
        }
        alg_selecionado = questionary.select(
            "Selecione o Algoritmo:",
            choices=list(alg_map.keys())
        ).ask()
        
        if not alg_selecionado: return

        n = click.prompt("Número de clientes", type=click.IntRange(min=1))

        pontos = []
        dep_str = click.prompt("Coordenadas do Depósito (x y)")
        xd, yd = map(float, dep_str.split())
        pontos.append((xd, yd))

        for i in range(n):
            cli_str = click.prompt(f"Coordenadas do Cliente {i+1} (x y)")
            x, y = map(float, cli_str.split())
            pontos.append((x, y))

        executar_teste_direto(alg_selecionado, n, pontos)
    except Exception as e:
        click.secho(f"Erro ao executar teste: {e}", fg="red")

def menu_interativo():
    click.clear()
    while True:
        try:
            opcao = questionary.select(
                "=== PLANEJAMENTO DE ROTAS DE ENTREGA (TSP) ===",
                choices=[
                    "Executar teste interativo",
                    "Ver relatório acumulado em memória",
                    "Salvar relatório acumulado em arquivo (.txt)",
                    "Gerar gráficos comparativos (N=3 a N=10)",
                    "Sair"
                ]
            ).ask()

            if opcao == "Sair" or not opcao:
                click.secho("Encerrando aplicação...", fg="yellow")
                break
            elif opcao == "Executar teste interativo":
                executar_teste()
            elif opcao == "Ver relatório acumulado em memória":
                relatorioController.imprimir_relatorios()
                click.pause()
            elif opcao == "Salvar relatório acumulado em arquivo (.txt)":
                nome = click.prompt("Nome do arquivo de saída", default="relatorio.txt")
                relatorioController.salvar_relatorios_txt(nome)
            elif opcao == "Gerar gráficos comparativos (N=3 a N=10)":
                click.secho("Executando simulações de benchmark...", fg="cyan", bold=True)
                graficoController.executar_testes_e_plotar()
                click.pause()
            
            click.clear()

        except (EOFError, KeyboardInterrupt):
            click.secho("\nEncerrando...", fg="yellow")
            break

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Sistema de Planejamento de Rotas de Entrega (Traveling Salesperson Problem - TSP)

    Se nenhum subcomando for fornecido, inicia o Menu Interativo automaticamente.
    """
    if ctx.invoked_subcommand is None:
        menu_interativo()

@cli.command("solve")
@click.option("-a", "--algorithm", type=click.Choice(["1", "2", "3", "4", "5"]), help="ID do Algoritmo: 1 (Branch & Bound), 2 (Backtracking), 3 (Prog. Dinâmica), 4 (Gulosa), 5 (2-Opt)")
@click.option("-n", "--nodes", type=click.IntRange(min=1), help="Número de clientes")
def solve_cmd(algorithm, nodes):
    """Executa a rota para uma instância específica (via parâmetros ou prompts)"""
    try:
        if algorithm is None or nodes is None:
            # Se algum estiver faltando, executa de forma interativa
            click.secho("Opções insuficientes passadas via CLI. Iniciando modo interativo para coletar dados.", fg="yellow")
            executar_teste()
            return

        click.secho(f"\nConfigurando execução para {nodes} clientes usando algoritmo {algorithm}...", fg="cyan")
        deposito_str = click.prompt(
            click.style("Coordenadas do Depósito (x y)", fg="green", bold=True),
            type=str
        )
        xd, yd = map(float, deposito_str.split())
        pontos = [(xd, yd)]

        for i in range(nodes):
            cliente_str = click.prompt(
                click.style(f"Coordenadas do Cliente {i+1} (x y)", fg="green", bold=True),
                type=str
            )
            x, y = map(float, cliente_str.split())
            pontos.append((x, y))

        executar_teste_direto(algorithm, nodes, pontos)
    except Exception as e:
        click.secho(f"Erro ao executar solução direta: {e}", fg="red")

@cli.command("benchmark")
@click.option("--min-n", type=int, default=3, show_default=True, help="Número mínimo de clientes")
@click.option("--max-n", type=int, default=10, show_default=True, help="Número máximo de clientes")
@click.option("--seed", type=int, default=42, show_default=True, help="Semente (seed) aleatória")
@click.option("--save-instances", is_flag=True, help="Salvar os dados das instâncias geradas")
@click.option("--out-dir", type=click.Path(), default="Relatorios", show_default=True, help="Diretório para salvar gráficos e CSV")
def benchmark_cmd(min_n, max_n, seed, save_instances, out_dir):
    """Executa simulações completas de benchmark e plota os gráficos comparativos"""
    try:
        click.secho(f"Iniciando simulações de benchmark (N de {min_n} até {max_n})...", fg="cyan", bold=True)
        ns = list(range(min_n, max_n + 1))
        graficoController.executar_testes_e_plotar(ns=ns, seed=seed, save_instances=save_instances, out_dir=out_dir)
        click.secho(f"Benchmark concluído! Arquivos salvos com sucesso em '{out_dir}'.", fg="green", bold=True)
    except Exception as e:
        click.secho(f"Erro ao rodar benchmark: {e}", fg="red")

if __name__ == "__main__":
    cli()
