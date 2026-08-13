# Estrutura do Projeto

## Organização das Pastas

```
📁 Projeto/
│
├── 📂 src/                        # Código-fonte principal
│   ├── 📂 Algoritmos/             # Implementações dos algoritmos
│   │   ├── Backtracking.py
│   │   ├── BranchAndBound.py
│   │   ├── EstrategiaGulosa.py
│   │   ├── ProgramacaoDinamica.py
│   │   └── TwoOpt.py
│   ├── 📂 Controller/             # Controllers de visualização e relatórios
│   │   ├── graficoController.py
│   │   └── relatorioController.py
│   ├── 📂 IO/                     # Input/Output de dados
│   │   ├── escritor_saida.py
│   │   └── leitor_entrada.py
│   ├── main.py                    # Arquivo principal de execução
│   └── Teste-graficos.py          # Script de testes de gráficos
│
├── 📂 scripts/                    # Scripts auxiliares
│   ├── run_benchmarks.py          # Script para executar benchmarks
│   ├── run_extended_benchmark.py  # Script de benchmark estendido
│   └── plot_benchmark.py          # Script para gerar gráficos de benchmark
│
├── 📂 output/                     # Resultados e relatórios
│   ├── benchmark_metrics.csv      # Métricas de performance
│   ├── grafico_comparativo.png
│   ├── grafico_estados_detalhado.png
│   ├── grafico_gap_detalhado.png
│   ├── grafico_memoria_detalhado.png
│   └── grafico_tempo_detalhado.png
│
├── 📂 docs/                       # Documentação
│   └── Documento/                 # Documentos do projeto
│       └── Relatório/             # Relatórios
│
├── requirements.txt               # Dependências do projeto
├── README.md                      # Documentação principal
└── .gitignore                     # Configurações do Git

```

## Descrição das Pastas

### `/src/` - Código-fonte
Contém todo o código principal da aplicação, organizado em módulos:
- **Algoritmos/**: Implementações dos algoritmos de otimização de rotas
- **Controller/**: Lógica de controle para gráficos e relatórios
- **IO/**: Funções de leitura e escrita de dados
- **main.py**: Ponto de entrada do programa
- **Teste-graficos.py**: Utilitário para testes visuais

### `/scripts/` - Scripts de Execução
Scripts auxiliares para benchmarking e análise:
- Execução de testes de performance
- Geração de gráficos comparativos
- Análise de dados

### `/output/` - Resultados
Saída gerada pela aplicação:
- Arquivos CSV com métricas
- Imagens de gráficos análise

### `/docs/` - Documentação
Documentação técnica e relatórios do projeto

## Como Executar

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

### Executar Programa Principal
```bash
python src/main.py
```

### Executar Benchmarks
```bash
python scripts/run_benchmarks.py
```

### Gerar Gráficos
```bash
python scripts/plot_benchmark.py
```

---
*Estrutura organizada para melhor mantenibilidade e escalabilidade do projeto.*
