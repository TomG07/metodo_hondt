# 🗳️ Método de Hondt - Simulador de Distribuição de Assentos

Um simulador interativo em Python do **Método de Hondt**, utilizado no sistema de eleição proporcional português para distribuir assentos parlamentares com base nos votos recebidos por cada partido.

## 📋 Sobre o Método de Hondt

O Método de Hondt é um sistema de distribuição proporcional de assentos utilizado em diversos países, incluindo Portugal. O método funciona da seguinte forma:

- Cada partido apresenta uma lista de candidatos
- Os eleitores votam numa lista partidária
- Os votos são contados e os assentos distribuídos proporcionalmente
- Utiliza divisores sucessivos para calcular quocientes
- O partido com maior quociente recebe o próximo assento
- O processo repete-se até todos os assentos serem distribuídos

Este método tende a favorecer partidos maiores, mas permite representação proporcional de partidos menores.

## ✨ Funcionalidades

- ✅ Entrada dinâmica de dados (número de partidos e votos)
- ✅ Cálculo automático de distribuição de assentos
- ✅ Suporte para qualquer número de partidos e assentos
- ✅ Resultados claros e organizados
- ✅ Interface simples via linha de comandos

## 🚀 Como Usar

### Pré-requisitos

- Python 3.6 ou superior instalado no seu sistema

### Instalação

1. Clone este repositório:

```bash
git clone https://github.com/TomG07/metodo_hondt.git
```

2. Navegue até à pasta do projeto:

```bash
cd metodo_hondt
```

### Execução

Execute o programa com Python:

```bash
python main.py
```

ou

```bash
python3 main.py
```

### Modo avançado (CSV e opções)

Também pode executar com ficheiro CSV e escolher estratégias de desempate e ordenação:

```bash
# CSV com colunas: partido,votos
python3 main.py --csv data/exemplo_partidos.csv --seats 7 --tie votes_alpha --show-table --sort-by seats
```

Opções disponíveis:

- `--csv`: caminho para o CSV com as colunas `partido,votos`
- `--seats`: número total de assentos a distribuir (obrigatório com `--csv`)
- `--tie`: estratégia de desempate (`votes`, `alpha`, `input`, `random`, `votes_alpha`)
- `--show-table`: mostra cada ronda com o vencedor e quociente
- `--sort-by`: `seats` | `votos` | `nome` (default: `seats`)
- `--asc`: ordena em ascendente (por defeito é descendente)

### Exportar resultados

```bash
# Exportar para CSV (resultados e rondas)
python3 main.py --csv data/exemplo_partidos.csv --seats 7 --out-csv outputs/resultados.csv

# Exportar para JSON (inclui tabela de rondas)
python3 main.py --csv data/exemplo_partidos.csv --seats 7 --out-json outputs/resultados.json
```

### Gráfico de Assentos

Requer instalar dependências:

```bash
python3 -m pip install -r requirements.txt
```

Gerar gráfico:

```bash
python3 main.py --csv data/exemplo_partidos.csv --seats 7 --graph outputs/assentos.png
```

### Testes

Instale dependências e execute:

```bash
python3 -m pip install -r requirements.txt
pytest -q
```

## 💡 Exemplo de Uso

```
Digite o número de partidos: 4
Digite o nome do partido: Partido A
Digite o número de votos para o partido Partido A: 340000
Digite o nome do partido: Partido B
Digite o número de votos para o partido Partido B: 280000
Digite o nome do partido: Partido C
Digite o número de votos para o partido Partido C: 160000
Digite o nome do partido: Partido D
Digite o número de votos para o partido Partido D: 60000
Digite o número total de assentos a distribuir: 7

Distribuição final dos assentos:
Partido: Partido A, Assentos: 3
Partido: Partido B, Assentos: 2
Partido: Partido C, Assentos: 1
Partido: Partido D, Assentos: 1
```

## 🔍 Como Funciona

O algoritmo implementa os seguintes passos:

1. **Definição dos Partidos**: Armazena o nome e votos de cada partido
2. **Cálculo de Quocientes**: Para cada iteração, calcula o quociente de cada partido usando a fórmula:
   $$\text{Quociente} = \frac{\text{Votos}}{\text{Assentos} + 1}$$
3. **Atribuição de Assentos**: O partido com maior quociente recebe um assento
4. **Repetição**: O processo repete-se até todos os assentos serem distribuídos

## 📁 Estrutura do Projeto

```
metodo_hondt/
├── main.py          # Código principal do simulador
└── README.md        # Este arquivo
```

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📜 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## 👤 Autor

**TomG07**

- GitHub: [@TomG07](https://github.com/TomG07)
- Repositório: [metodo_hondt](https://github.com/TomG07/metodo_hondt)
- Instagram: [@tomfraza0](https://instagram.com/tomfraza0)
- [Website](https://www.tomasfrazao.eu)

---

⭐ Se este projeto foi útil, considere dar uma estrela no repositório!
