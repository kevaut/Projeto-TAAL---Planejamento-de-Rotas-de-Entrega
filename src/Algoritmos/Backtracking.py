class Backtracking:
    def __init__(self, matriz_dist):
        self.matriz_dist = matriz_dist
        self.n = len(matriz_dist) - 1
        self.melhor_distancia = float('inf')
        self.melhor_rota = []
        self.estados_explorados = 0
        self.chamadas_recursivas = 0
        self.podas = 0
        self.profundidade_max = 0

    def resolver(self):
        self._backtracking(0, {0}, [0], 0.0, 0)
        return self.melhor_distancia, self.melhor_rota, self.estados_explorados

    def _backtracking(self, atual, visitados, rota_atual, dist_atual, profundidade):
        self.estados_explorados += 1
        self.chamadas_recursivas += 1
        if profundidade > self.profundidade_max:
            self.profundidade_max = profundidade

        # Poda por custo: se a distância acumulada já supera a melhor
        # solução conhecida, não há sentido em continuar este ramo.
        if dist_atual >= self.melhor_distancia:
            self.podas += 1
            return

        # Caso base: todos os nós foram visitados → fecha o ciclo
        if len(visitados) == self.n + 1:
            d = dist_atual + self.matriz_dist[atual][0]
            if d < self.melhor_distancia:
                self.melhor_distancia = d
                self.melhor_rota = rota_atual.copy()
            return

        for prox in range(1, self.n + 1):
            if prox not in visitados:
                visitados.add(prox)
                rota_atual.append(prox)
                self._backtracking(
                    prox,
                    visitados,
                    rota_atual,
                    dist_atual + self.matriz_dist[atual][prox],
                    profundidade + 1
                )
                rota_atual.pop()
                visitados.remove(prox)
