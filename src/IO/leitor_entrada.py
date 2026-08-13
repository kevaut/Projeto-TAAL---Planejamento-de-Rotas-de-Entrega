def ler_dados_teste():
    print("\n1 - Branch and Bound")
    print("2 - Backtracking")
    print("3 - Programação Dinâmica")
    print("4 - Estratégia Gulosa")
    print("5 - 2-Opt (heurística de melhoria)")
    alg = input("Algoritmo: ").strip()

    if alg not in ("1", "2", "3", "4", "5"):
        raise ValueError("Algoritmo inválido")

    n = int(input("Número de clientes: ").strip())
    if n <= 0:
        raise ValueError("Número de clientes inválido")

    xd, yd = map(float, input("Depósito (x y): ").split())
    pontos = [(xd, yd)]

    for i in range(n):
        x, y = map(float, input(f"Cliente {i+1} (x y): ").split())
        pontos.append((x, y))
        
    return alg, n, pontos

def ler_opcao_menu():
    return input("Opção: ").strip()

def ler_nome_arquivo():
    return input("Nome do arquivo (.txt): ").strip()
