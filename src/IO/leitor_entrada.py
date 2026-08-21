import click

def ler_dados_teste():
    click.echo(click.style("\n=== SELEÇÃO DE ALGORITMO ===", fg="cyan", bold=True))
    click.echo("1 - Branch and Bound")
    click.echo("2 - Backtracking")
    click.echo("3 - Programação Dinâmica")
    click.echo("4 - Estratégia Gulosa")
    click.echo("5 - 2-Opt (heurística de melhoria)")
    
    alg = click.prompt(
        click.style("Selecione o Algoritmo", fg="green", bold=True),
        type=click.Choice(["1", "2", "3", "4", "5"]),
        show_choices=True
    )

    n = click.prompt(
        click.style("Número de clientes", fg="green", bold=True),
        type=click.IntRange(min=1)
    )

    deposito_str = click.prompt(
        click.style("Coordenadas do Depósito (x y)", fg="green", bold=True),
        type=str
    )
    try:
        xd, yd = map(float, deposito_str.split())
    except Exception:
        raise click.UsageError("As coordenadas do depósito devem ser dois números reais separados por espaço.")
        
    pontos = [(xd, yd)]

    for i in range(n):
        cliente_str = click.prompt(
            click.style(f"Coordenadas do Cliente {i+1} (x y)", fg="green", bold=True),
            type=str
        )
        try:
            x, y = map(float, cliente_str.split())
        except Exception:
            raise click.UsageError(f"As coordenadas do cliente {i+1} devem ser dois números reais separados por espaço.")
        pontos.append((x, y))
        
    return alg, n, pontos

def ler_opcao_menu():
    return click.prompt(
        click.style("Selecione uma opção", fg="green", bold=True),
        type=click.Choice(["0", "1", "2", "3", "4"]),
        show_choices=False
    )

def ler_nome_arquivo():
    return click.prompt(
        click.style("Nome do arquivo de saída (.txt)", fg="green", bold=True),
        type=str,
        default="relatorio.txt"
    )
