# CloudWalk - Monitoring Intelligence Analyst Challenge

Este repositório contém a solução completa para o desafio técnico da CloudWalk para a posição de Monitoring Intelligence Analyst (Night Shift).

## 📋 Estrutura do Projeto

monitoring-challenge/
│
├── part1_analysis/ # Análise Exploratória
│ ├── analise_checkout.py # Script principal de análise
│ ├── checkout_2.csv # Dataset de vendas por hora
│ └── README.md # Documentação da Parte 1
│
├── part2_monitoring/ # Sistema de Monitoramento
│ ├── app.py # Endpoint Flask
│ ├── dashboard.py # Dashboard em tempo real
│ ├── detector.py # Modelo de detecção de anomalias
│ ├── alert_system.py # Sistema de alertas
│ ├── simulate.py # Simulador de transações
│ ├── transactional_data.csv # Dataset de transações
│ ├── transactional_data_2.csv # Segundo dataset
│ └── README.md # Documentação da Parte 2
│
├── .gitignore
├── requirements.txt # Dependências do projeto
└── README.md # Este arquivo

## 🚀 Como Executar

### Parte 1 - Análise Exploratória

```bash
cd part1_analysis
python analise_checkout.py
cd part2_monitoring

# Instalar dependências
pip install -r requirements.txt

# Terminal 1 - Endpoint
python app.py

# Terminal 2 - Dashboard
python dashboard.py

# Terminal 3 - Simulador
python simulate.py
```

## 📊 Resultados
* Parte 1: Identificadas 7 horas com anomalias (29% do dia)

* Parte 2: Sistema de alertas com detecção em tempo real

## 🛠️ Tecnologias Utilizadas
* Python 3.12

* Pandas / NumPy

* Flask (API REST)

* Plotly Dash (Dashboard)

* SQLite (Banco de dados)

## 📌 Autor
### Rui Penteado - rp.augusto@hotmail.com

---

### **2.3 - Criar README da Parte 1**

Crie o arquivo **`part1_analysis/README.md`** com o conteúdo que fizemos anteriormente (a descrição completa da Parte 1).

---

### **2.4 - Criar README da Parte 2**

Crie o arquivo **`part2_monitoring/README.md`** com o conteúdo que fizemos anteriormente (a descrição completa da Parte 2).

---

### **2.5 - Criar requirements.txt na raiz**

Crie o arquivo **`requirements.txt`** na raiz do projeto:

```t
# Core
pandas==2.2.3
numpy==1.26.4

# API
flask==2.3.3
requests==2.32.3

# Dashboard
plotly==5.22.0
dash==2.17.1

# Utils
setuptools
wheel
```