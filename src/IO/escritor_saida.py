def imprimir_menu():
    print("\n=== Planejamento de Rotas de Entrega ===")
    print("1 - Executar teste")
    print("2 - Ver relatório")
    print("3 - Salvar relatório em arquivo")
    print("4 - Gerar gráficos comparativos")
    print("0 - Sair")

def imprimir_resultado(distancia, rota):
    rota_str = "0 " + " ".join(map(str, rota)) + " 0"
    print(f"\nDistância: {distancia:.6f}")
    print(f"Rota     : {rota_str}")

def imprimir_mensagem(msg):
    print(msg)
