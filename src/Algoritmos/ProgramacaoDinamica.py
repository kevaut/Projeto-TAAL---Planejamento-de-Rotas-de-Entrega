class ProgramacaoDinamica:
    def __init__(self, matriz_dist):
        self.matriz_dist = matriz_dist
        self.n = len(matriz_dist) - 1
        self.memo = {}
        self.parent = {}
        self.estados_explorados = 0
        self.chamadas_recursivas = 0
        self.podas = 0
        self.profundidade_max = 0
        self.melhor_distancia = float('inf')
        self.melhor_rota = []

    def resolver(self):
        visitados_bitmask = 1 << 0
        self.melhor_distancia = self._tsp(0, visitados_bitmask, 0)
        
        atual = 0
        mask = visitados_bitmask
        
        while True:
            prox_nodo = self.parent.get((atual, mask))
            # Proteção: None indica ausência de registro (rota completa)
            # -1 indica que nenhum vizinho foi encontrado (grafo inválido)
            if prox_nodo is None or prox_nodo == -1:
                break
            self.melhor_rota.append(prox_nodo)
            mask = mask | (1 << prox_nodo)
            atual = prox_nodo
            
        return self.melhor_distancia, self.melhor_rota, self.estados_explorados

    def _tsp(self, u, mask, profundidade):
        self.estados_explorados += 1
        self.chamadas_recursivas += 1
        if profundidade > self.profundidade_max:
            self.profundidade_max = profundidade

        # Caso base: todos os clientes e depósito foram visitados
        if mask == (1 << (self.n + 1)) - 1:
            return self.matriz_dist[u][0]
            
        # Se o subproblema já foi computado, retorna
        if (u, mask) in self.memo:
            return self.memo[(u, mask)]
            
        ans = float('inf')
        melhor_v = -1
        
        for v in range(1, self.n + 1):
            # Se v não foi visitado ainda
            if (mask & (1 << v)) == 0:
                dist = self.matriz_dist[u][v] + self._tsp(v, mask | (1 << v), profundidade + 1)
                if dist < ans:
                    ans = dist
                    melhor_v = v
                    
        self.memo[(u, mask)] = ans
        self.parent[(u, mask)] = melhor_v
        return ans
