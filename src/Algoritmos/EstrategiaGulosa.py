class EstrategiaGulosa:
    def __init__(self, matriz_dist):
        self.matriz_dist = matriz_dist
        self.n = len(matriz_dist) - 1
        self.melhor_distancia = 0.0
        self.melhor_rota = []
        self.estados_explorados = 0
        self.chamadas_recursivas = 0
        self.podas = 0
        self.profundidade_max = 0

    def resolver(self):
        visitados = {0}
        atual = 0
        self.profundidade_max = 1
        for _ in range(self.n):
            self.estados_explorados += 1 
            self.chamadas_recursivas += 1
            prox = -1
            menor_dist = float('inf')
            
            for i in range(1, self.n + 1):
                if i not in visitados:
                    if self.matriz_dist[atual][i] < menor_dist:
                        menor_dist = self.matriz_dist[atual][i]
                        prox = i
                        
            visitados.add(prox)
            self.melhor_rota.append(prox)
            self.melhor_distancia += menor_dist
            atual = prox
            
        # Fim: retorna para o depósito
        self.melhor_distancia += self.matriz_dist[atual][0]
        self.estados_explorados += 1
        
        return self.melhor_distancia, self.melhor_rota, self.estados_explorados
