class BranchAndBound:
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
        self._branch_and_bound(0, {0}, [0], 0.0, 0)
        return self.melhor_distancia, self.melhor_rota, self.estados_explorados

    def _lower_bound(self, atual, visitados, dist_atual):
        """
        Limitante inferior (lower bound) para o custo de completar a rota.

        Para cada nó relevante (nó atual + nós não visitados), calcula a
        menor aresta de saída possível em direção aos destinos restantes
        (não visitados + depósito de retorno). A soma dessas mínimas
        arestas é um limitante inferior válido: qualquer rota que complete
        o ciclo precisa atravessar pelo menos uma aresta a partir de cada
        um desses nós.
        """
        nao_visitados = [i for i in range(self.n + 1) if i not in visitados]

        # Todos os nós já visitados → só falta retornar ao depósito
        if not nao_visitados:
            return dist_atual + self.matriz_dist[atual][0]

        # Destinos candidatos: não visitados + depósito (retorno final)
        restantes = nao_visitados + [0]

        lb = 0

        # Custo mínimo de sair do nó atual em direção a algum restante
        lb += min(self.matriz_dist[atual][v] for v in restantes)

        # Para cada nó não visitado, custo mínimo de saída para outro restante
        for v in nao_visitados:
            outros = [u for u in restantes if u != v]
            if outros:
                lb += min(self.matriz_dist[v][u] for u in outros)

        return dist_atual + lb

    def _branch_and_bound(self, atual, visitados, rota_atual, dist_atual, profundidade):
        self.estados_explorados += 1
        self.chamadas_recursivas += 1
        if profundidade > self.profundidade_max:
            self.profundidade_max = profundidade

        # Poda por limitante inferior: se o mínimo possível para completar
        # já supera a melhor solução conhecida, abandona este ramo inteiro.
        if self._lower_bound(atual, visitados, dist_atual) >= self.melhor_distancia:
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
                self._branch_and_bound(
                    prox,
                    visitados,
                    rota_atual,
                    dist_atual + self.matriz_dist[atual][prox],
                    profundidade + 1
                )
                rota_atual.pop()
                visitados.remove(prox)
