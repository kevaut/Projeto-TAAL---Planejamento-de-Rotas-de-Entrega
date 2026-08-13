class TwoOpt:
    def __init__(self, matriz_dist):
        self.matriz_dist = matriz_dist
        self.n = len(matriz_dist) - 1
        self.melhor_distancia = float('inf')
        self.melhor_rota = []
        self.estados_explorados = 0
        self.chamadas_recursivas = 0
        self.podas = 0
        self.profundidade_max = 0

    def _route_distance(self, route):
        d = 0.0
        for i in range(len(route) - 1):
            d += self.matriz_dist[route[i]][route[i+1]]
        return d

    def resolver(self):
        # usa vizinho mais próximo como solução inicial
        from Algoritmos.EstrategiaGulosa import EstrategiaGulosa
        greedy = EstrategiaGulosa(self.matriz_dist)
        dist_g, route_g, _ = greedy.resolver()

        # rota interna com depósito nas extremidades: 0 ... 0
        route = [0] + route_g + [0]
        best = self._route_distance(route)
        improved = True
        self.estados_explorados = 0
        self.chamadas_recursivas = 0

        while improved:
            improved = False
            n = len(route)
            for i in range(1, n - 2):
                for k in range(i + 1, n - 1):
                    self.estados_explorados += 1
                    # custo antes
                    d_before = self.matriz_dist[route[i-1]][route[i]] + self.matriz_dist[route[k]][route[k+1]]
                    # custo depois da troca
                    d_after = self.matriz_dist[route[i-1]][route[k]] + self.matriz_dist[route[i]][route[k+1]]
                    if d_after < d_before - 1e-9:
                        # aplica 2-opt (reverte segmento)
                        route[i:k+1] = list(reversed(route[i:k+1]))
                        best = best - d_before + d_after
                        improved = True
                        self.chamadas_recursivas += 1
            # itera até nenhum melhoramento

        self.melhor_distancia = best
        # armazena rota sem depósito nas extremidades (consistente com outros solvers)
        self.melhor_rota = route[1:-1]
        return self.melhor_distancia, self.melhor_rota, self.estados_explorados
