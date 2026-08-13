import os

relatorios = []
def adicionar_relatorio(relatorio):
    relatorios.append(relatorio)

def imprimir_relatorios():
    if not relatorios:
        print("\nNenhum teste registrado.")
        return

    print("\n========= RELATÓRIO GERAL =========")
    for i, r in enumerate(relatorios, 1):
        print(f"\nTeste #{i}")
        print(f"Algoritmo : {r['algoritmo']}")
        print(f"Clientes  : {r['n']}")
        print(f"Status    : {r['status']}")
        print(f"Tempo     : {r['tempo']:.6f} s")
        print(f"Estados   : {r['estados']}")
        if r.get('memoria_peak') is not None:
            print(f"Memória peak : {r['memoria_peak']:.3f} KB")
        if r.get('chamadas_recursivas') is not None:
            print(f"Chamadas rec.: {r.get('chamadas_recursivas')}")
        if r.get('podas') is not None:
            print(f"Podas       : {r.get('podas')}")
        if r.get('profundidade_max') is not None:
            print(f"Profundidade : {r.get('profundidade_max')}")

        if r["status"] == "Sucesso":
            print(f"Distância : {r['distancia']:.6f}")
            print(f"Rota      : {r['rota']}")
        else:
            print(f"Erro      : {r['erro']}")


def salvar_relatorios_txt(nome):
    if not relatorios:
        print("\nNenhum teste para salvar.")
        return
    pasta = "Relatorios"
    os.makedirs(pasta, exist_ok=True)
    caminho_completo = os.path.join(pasta, nome)
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE TESTES - TSP\n")
        f.write("=" * 60 + "\n\n")

        for i, r in enumerate(relatorios, 1):
            f.write(f"Teste #{i}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Algoritmo : {r['algoritmo']}\n")
            f.write(f"Clientes  : {r['n']}\n")
            f.write(f"Status    : {r['status']}\n")
            f.write(f"Tempo     : {r['tempo']:.6f} s\n")
            f.write(f"Estados   : {r['estados']}\n")
            if r.get('memoria_peak') is not None:
                f.write(f"Memória peak : {r['memoria_peak']:.3f} KB\n")
            if r.get('chamadas_recursivas') is not None:
                f.write(f"Chamadas rec.: {r.get('chamadas_recursivas')}\n")
            if r.get('podas') is not None:
                f.write(f"Podas       : {r.get('podas')}\n")
            if r.get('profundidade_max') is not None:
                f.write(f"Profundidade : {r.get('profundidade_max')}\n")

            if r["status"] == "Sucesso":
                f.write(f"Distância : {r['distancia']:.6f}\n")
                f.write(f"Rota      : {r['rota']}\n")
            else:
                f.write(f"Erro      : {r['erro']}\n")

            f.write("\n")

    print(f"\nRelatório salvo em '{nome}'")
