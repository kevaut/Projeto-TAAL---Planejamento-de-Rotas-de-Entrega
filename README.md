# Técnicas de Análise de Algoritmos — Planejamento de Rotas de Entrega

Projeto didático que implementa e compara quatro estratégias algorítmicas para o
**Problema do Caixeiro Viajante (TSP)** aplicado ao planejamento de rotas de entrega.
Um veículo parte de um depósito, visita todos os clientes exatamente uma vez e
retorna ao depósito, minimizando a distância total percorrida.

---

## Sumário

1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Formato de Entrada e Saída](#formato-de-entrada-e-saída)
3. [Como Executar](#como-executar)
4. [Algoritmos Implementados](#algoritmos-implementados)
5. [Análise Comparativa](#análise-comparativa)
   - [Complexidade Assintótica](#1-complexidade-assintótica-teórica)
   - [Tempo de Execução](#2-tempo-de-execução-empírico)
   - [Uso de Memória](#3-uso-de-memória)
   - [Qualidade da Solução](#4-qualidade-da-solução-ótima-vs-aproximada)
   - [Escalabilidade](#5-escalabilidade)
   - [Métricas de Estados Explorados](#6-métricas-de-estados-explorados)
   - [Podas e Justificativas](#7-podas-no-espaço-de-busca-e-justificativas)
6. [Observações](#observações)

---

## Estrutura do Projeto

```
.
├── main.py                      # Programa principal — menu interativo
├── Algoritmos/
│   ├── Backtracking.py          # Busca exaustiva DFS com poda por custo
│   ├── BranchAndBound.py        # B&B com limitante inferior real (lower bound)
│   ├── ProgramacaoDinamica.py   # Held-Karp com bitmask e memoização
│   └── EstrategiaGulosa.py      # Heurística do vizinho mais próximo
├── Controller/
│   ├── relatorioController.py   # Gerencia relatórios em memória e em arquivo
│   └── graficoController.py     # Benchmarks automáticos e gráficos comparativos
├── IO/
│   ├── leitor_entrada.py        # Leitura de dados do usuário (menu, coordenadas)
│   └── escritor_saida.py        # Impressão de resultados e mensagens
├── Relatorios/                  # Relatórios .txt salvos e gráfico PNG gerado
└── Documento/                   # Documentos de análise formais (PDF/DOCX)
```

Cada algoritmo em `Algoritmos/` expõe a mesma interface:

```python
solver = Algoritmo(matriz_distancias)
melhor_distancia, melhor_rota, estados_explorados = solver.resolver()
```

---

## Formato de Entrada e Saída

### Entrada (via prompt interativo)

```
n                    ← número de clientes
xd yd                ← coordenadas do depósito
x1 y1                ← coordenadas do cliente 1
x2 y2
...
xn yn
```

**Exemplo (5 clientes):**
```
5
0 0
2 3
5 2
6 6
8 3
1 7
```

### Saída

```
distancia_total
0 c1 c2 c3 ... cn 0
```

**Exemplo:**
```
24.9807
0 1 2 4 3 5 0
```

> A distância entre dois pontos é calculada via **distância Euclidiana**:
> `d(i,j) = sqrt((xi-xj)² + (yi-yj)²)`
> O índice `0` representa o depósito; `ci` representa o i-ésimo cliente.

---

## Como Executar

1. Crie e ative um ambiente virtual (opcional):

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Instale a dependência para geração de gráficos:

```powershell
pip install matplotlib
```

3. Execute o programa:

```powershell
python main.py
```

4. **Menu disponível:**

| Opção | Ação |
|:---:|---|
| `1` | Executar teste — informa algoritmo, nº de clientes e coordenadas |
| `2` | Ver relatório — imprime todos os testes registrados na sessão |
| `3` | Salvar relatório em arquivo `.txt` na pasta `Relatorios/` |
| `4` | Gerar gráficos comparativos — benchmarks automáticos com matplotlib |
| `0` | Sair |

---

## Algoritmos Implementados

### `Backtracking.py` — Classe `Backtracking`
Busca exaustiva em profundidade (DFS) que percorre todas as permutações possíveis
de visita aos clientes. A poda é feita assim que o custo acumulado supera a melhor
solução conhecida, evitando expandir ramos claramente inviáveis.

### `BranchAndBound.py` — Classe `BranchAndBound`
Extensão do Backtracking com um **limitante inferior real** (`_lower_bound`):
para o nó atual e cada nó ainda não visitado, calcula a menor aresta de saída
possível em direção aos destinos restantes (incluindo o retorno ao depósito).
Se essa estimativa mínima já supera a melhor solução conhecida, o ramo inteiro
é podado antes de ser expandido — reduzindo o espaço de busca em 50–90%.

### `ProgramacaoDinamica.py` — Classe `ProgramacaoDinamica`
Implementação do algoritmo **Held-Karp** com bitmask. Usa memoização para
armazenar o resultado de cada subproblema `(nó_atual, máscara_de_visitados)`,
eliminando recálculos e reduzindo a complexidade de $O(N!)$ para $O(N^2 \cdot 2^N)$.
Reconstrói a rota ótima via tabela de predecessores `parent`.

### `EstrategiaGulosa.py` — Classe `EstrategiaGulosa`
Heurística do **vizinho mais próximo** (Nearest-Neighbor): a partir do depósito,
escolhe sempre o cliente não visitado mais próximo do nó atual. Extremamente
rápida $O(N^2)$ mas não garante a solução ótima — pode produzir rotas
sub-ótimas quando os saltos finais são forçados a longas distâncias.

---

## Análise Comparativa

### 1. Complexidade Assintótica (Teórica)

| Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :---: | :---: |
| **Backtracking** | $O(N!)$ | $O(N)$ |
| **Branch and Bound** | $O(N!)$ no pior caso | $O(N)$ |
| **Programação Dinâmica** | $O(N^2 \cdot 2^N)$ | $O(N \cdot 2^N)$ |
| **Estratégia Gulosa** | $O(N^2)$ | $O(N)$ |

> **Nota:** B&B tem o mesmo pior caso que Backtracking pois, quando nenhuma poda
> ocorre, percorre a mesma árvore permutacional. Na prática, o limitante inferior
> reduz drasticamente o número de nós expandidos. O algoritmo Held-Karp (PD)
> transforma a explosão fatorial em exponencial pela eliminação de subproblemas
> sobrepostos via memoização.

---

### 2. Tempo de Execução (Empírico)

Testes rodados com a função de benchmark do `graficoController` (N = 3 a 10,
coordenadas aleatórias) demonstraram na prática as distinções teóricas:

| Algoritmo | Comportamento observado |
| :--- | :--- |
| **Gulosa** | < 0,001 s mesmo para N = 10; praticamente imediato |
| **PD** | Dezenas de ms até N = 10; cresce rapidamente após N ≈ 20 |
| **Branch and Bound** | Significativamente mais rápido que Backtracking graças ao `_lower_bound`; começa a crescer em N ≈ 12 |
| **Backtracking** | Supera 1 s em N = 10; inviável para N ≥ 12 |

> O gráfico comparativo é gerado automaticamente pela opção `4` do menu
> e salvo em `Relatorios/grafico_comparativo.png`.

---

### 3. Uso de Memória

| Algoritmo | Espaço | Detalhe |
| :--- | :---: | :--- |
| **Backtracking** | $O(N)$ | Apenas a pilha de recursão (DFS) |
| **Branch and Bound** | $O(N)$ | Apenas a pilha de recursão (DFS) |
| **Programação Dinâmica** | $O(N \cdot 2^N)$ | Tabela de memoização: até $2^N$ máscaras × $N$ nós |
| **Estratégia Gulosa** | $O(N)$ | Lista de visitados e rota atual |

O único algoritmo com crescimento de memória expressivo é a **Programação
Dinâmica**: para N = 20 já requer centenas de MB; para N = 25 pode chegar a
dezenas de GB, tornando-se inviável em hardware convencional.

---

### 4. Escalabilidade

| Algoritmo | Limite prático | Razão |
| :--- | :---: | :--- |
| **Gulosa** | N > 10.000 | Complexidade polinomial $O(N^2)$ |
| **PD (Held-Karp)** | N ≈ 20–25 | Memória exponencial $O(N \cdot 2^N)$ |
| **Branch and Bound** | N ≈ 20–30 | Podas eficazes, mas pior caso exponencial |
| **Backtracking** | N ≈ 11–12 | Sem limitante inferior, explora N! estados |

---

### 5. Métricas de Estados Explorados

Medidas coletadas nos benchmarks automáticos (opção `4`):

- **Backtracking** — gera o maior volume de estados; a única poda é por custo
  acumulado, o que só elimina ramos depois de um custo já comprometido.

- **Branch and Bound** — reduz em média **50% a 90%** os estados em relação ao
  Backtracking. Para cada nó, a função `_lower_bound` calcula a soma das menores
  arestas de saída de todos os nós restantes; se esse mínimo já supera a melhor
  solução, todo o sub-ramo é descartado antes de ser expandido.

- **Programação Dinâmica** — o número de estados únicos computados é limitado a
  $N \cdot 2^N$ (cada par `(nó, máscara)` é resolvido uma única vez). Para N = 10
  isso representa ≈ 10.240 estados, contra milhões no Backtracking.

- **Gulosa** — explora exatamente $N$ passos (um por cliente), sem backtracking.

---

### 6. Podas no Espaço de Busca e Justificativas

#### Branch and Bound — Limitante Inferior (`_lower_bound`)

A poda é aplicada **antes** de expandir qualquer filho do nó atual:

```python
if self._lower_bound(atual, visitados, dist_atual) >= self.melhor_distancia:
    return  # descarta todo o ramo
```

O limitante inferior é calculado como:

> Para o nó atual e para cada nó ainda não visitado, identifica-se a **menor
> aresta de saída possível** em direção a qualquer destino restante (clientes
> não visitados + depósito de retorno). A soma dessas mínimas arestas é um
> **limitante inferior válido**: qualquer conclusão de rota a partir deste estado
> precisa atravessar pelo menos essas arestas.

**Justificativa matemática:** se o menor custo possível para concluir a rota já
é ≥ à melhor solução conhecida, é **matematicamente impossível** que qualquer
permutação descendente produza um resultado melhor. Toda a sub-árvore é podada
em $O(N)$, em vez de ser explorada em $O(K!)$.

#### Programação Dinâmica — Subestrutura Ótima e Memoização

```python
if (u, mask) in self.memo:
    return self.memo[(u, mask)]
```

**Justificativa:** a menor rota de um nó `u` para completar o conjunto restante
`{X, Y, Z, ...}` é **independente do caminho percorrido antes de chegar em `u`**.
Ao armazenar esse resultado no dicionário `memo`, todos os galhos da árvore que
chegam em `u` com o mesmo conjunto de visitados compartilham o mesmo resultado —
reduzindo a complexidade de $O(N!)$ para $O(N^2 \cdot 2^N)$.

---

## Observações

- O código tem **intenção didática**; para $N > 11$ o Backtracking ficará muito lento.
- A matriz de distâncias é indexada com o **depósito no índice `0`** e os
  clientes nos índices `1` a `N`.
- Os benchmarks do `graficoController` usam coordenadas geradas aleatoriamente
  (N = 3 a 10); o gráfico é salvo automaticamente em `Relatorios/grafico_comparativo.png`.
- Para instâncias reais grandes, considere algoritmos aproximados como
  2-opt, Lin-Kernighan ou metaheurísticas (Simulated Annealing, Algoritmos Genéticos).
