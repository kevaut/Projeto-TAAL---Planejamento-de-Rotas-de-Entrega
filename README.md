# Técnicas de Análise de Algoritmos — Planejamento de Rotas de Entrega

Projeto didático que implementa e compara cinco estratégias algorítmicas para o
**Problema do Caixeiro Viajante (TSP)** aplicado ao planejamento de rotas de entrega.
Um veículo parte de um depósito, visita todos os clientes exatamente uma vez e
retorna ao depósito, minimizando a distância total percorrida.

---

## Sumário

1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Usabilidade](#usabilidade)
3. [Formato de Entrada e Saída](#formato-de-entrada-e-saída)
4. [Como Executar](#como-executar)
5. [Algoritmos Implementados](#algoritmos-implementados)
6. [Análise Comparativa](#análise-comparativa)
7. [Observações](#observações)

---

## Estrutura do Projeto

```
.
├── src/
│   ├── main.py                  # CLI principal baseada em Click
│   ├── Algoritmos/              # Implementações (Backtracking, B&B, PD, Gulosa, 2-Opt)
│   ├── Controller/              # Lógica de relatórios e geração de gráficos
│   └── IO/                      # I/O de dados
├── scripts/                     # Scripts de benchmark estendido
├── Relatorios/                  # Resultados (CSV e PNG) gerados
└── tests/                       # Testes automatizados (pytest)
```

---

## Usabilidade

O projeto conta com uma interface de linha de comando (CLI) robusta. Você pode utilizá-la de duas formas:

### 1. Modo Interativo (Menu via Teclado)
Inicie o menu interativo executando o programa sem argumentos:
```bash
python src/main.py
```
O menu utiliza navegação moderna com **setas do teclado** e **Enter** para seleção (implementado via `questionary`). Siga as instruções na tela para executar testes, ver relatórios ou gerar gráficos.

### 2. Modo de Linha de Comando (CLI Pro)
Para automação ou execuções rápidas, utilize os subcomandos baseados na biblioteca **Click**:

#### Resolver uma instância específica
```bash
# Executa um algoritmo específico para uma instância
python src/main.py solve --algorithm 1 --nodes 5
```
*(Se omitir parâmetros, o programa solicitará os dados via prompt).*

#### Executar Benchmarks Automatizados
```bash
# Executa benchmarks para um intervalo de N e gera gráficos automaticamente
python src/main.py benchmark --min-n 3 --max-n 10 --seed 42
```

Use `--help` para ver todas as opções:
```bash
python src/main.py --help
python src/main.py solve --help
python src/main.py benchmark --help
```

---

## Formato de Entrada e Saída

### Entrada (via prompt ou stdin)
O sistema espera o número de clientes, seguido pelas coordenadas `(x, y)` do depósito, e então as coordenadas `(x, y)` de cada um dos `n` clientes.

### Saída
```
Distância: <valor>
Rota     : 0 <c1> <c2> ... <cn> 0
```

> A distância entre dois pontos é calculada via **distância Euclidiana**.

---

## Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute via CLI (como descrito na seção [Usabilidade](#usabilidade)).

---

## Algoritmos Implementados

O projeto implementa cinco abordagens:
- **Backtracking**: Busca exaustiva com poda por custo.
- **Branch and Bound**: Busca otimizada com limitante inferior (lower bound).
- **Programação Dinâmica (Held-Karp)**: Otimização com bitmask e memoização.
- **Estratégia Gulosa**: Heurística de vizinho mais próximo.
- **2-Opt**: Heurística de refinamento local para melhoria de rotas.

---

## Análise Comparativa

*(Resumo dos algoritmos)*

| Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :---: | :---: |
| **Backtracking** | $O(N!)$ | $O(N)$ |
| **Branch and Bound** | $O(N!)$ | $O(N)$ |
| **Programação Dinâmica** | $O(N^2 \cdot 2^N)$ | $O(N \cdot 2^N)$ |
| **Estratégia Gulosa** | $O(N^2)$ | $O(N)$ |
| **2-Opt** | $O(I \cdot N^2)$ | $O(N)$ |

---

## Observações

- O código tem **intenção didática**.
- Benchmarks automáticos salvam arquivos em `Relatorios/`.
- Para instâncias grandes, priorize heurísticas como **2-Opt**.
