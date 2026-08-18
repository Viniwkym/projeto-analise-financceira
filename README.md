# 📊 Sistema de Análise de Saúde Financeira Empresarial

Uma aplicação web desenvolvida em Python com Streamlit para análise automatizada de saúde financeira de empresas a partir de Balanço Patrimonial e Demonstração do Resultado do Exercício (DRE).

## 🎯 Funcionalidades

- **Upload de Dados Financeiros**: Importação de arquivos CSV com dados históricos de 3 a 5 anos
- **Cálculo Automático de 8 Indicadores Fundamentais**:
  - Liquidez Corrente
  - Liquidez Seca
  - Endividamento Geral
  - Dívida Líquida / EBITDA
  - Margem EBITDA
  - Margem Líquida
  - ROE (Return on Equity)
  - Fluxo de Caixa Operacional / Dívida Total
- **Dashboard Interativo**: Visualização gráfica da evolução histórica dos indicadores
- **Diagnóstico Inteligente**: Identificação automática de problemas críticos e alertas
- **Recomendações Práticas**: Sugestões de soluções táticas para cada problema identificado

## 📋 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Configuração

### Windows

1. **Clone ou baixe o projeto**:
   ```cmd
   cd C:\Users\SeuUsuario
   git clone <url-do-repositorio>
   cd projeto-analise-financeira
   ```

2. **Crie um ambiente virtual**:
   ```cmd
   python -m venv venv
   ```

3. **Ative o ambiente virtual**:
   ```cmd
   venv\Scripts\activate
   ```

4. **Instale as dependências**:
   ```cmd
   pip install -r requirements.txt
   ```

### Linux/macOS

1. **Clone ou baixe o projeto**:
   ```bash
   cd ~
   git clone <url-do-repositorio>
   cd projeto-analise-financeira
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```

3. **Ative o ambiente virtual**:
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Como Executar

1. **Certifique-se de que o ambiente virtual está ativado** (você verá `(venv)` no início da linha de comando)

2. **Execute a aplicação**:
   ```bash
   streamlit run app.py
   ```

3. **Acesse a aplicação**: O navegador abrirá automaticamente em `http://localhost:8501`

## 🧪 Executando os Testes

Para garantir que tudo está funcionando corretamente, execute a suíte de testes:

```bash
pytest
```

Para ver mais detalhes sobre os testes:

```bash
pytest -v
```

Para ver a cobertura de testes:

```bash
pytest --cov=src tests/
```

## 📊 Como Usar a Aplicação

### 1. Preparar os Dados

Baixe o modelo de exemplo CSV disponível na interface da aplicação. O arquivo deve seguir o seguinte formato:

```csv
Conta,2021,2022,2023,2024,2025
Receita Líquida,1000000,1200000,1500000,1800000,2000000
EBITDA,200000,250000,300000,350000,400000
Lucro Líquido,80000,100000,120000,140000,160000
Ativo Circulante,500000,600000,750000,900000,1000000
Ativo Total,1500000,1800000,2250000,2700000,3000000
Estoque,150000,180000,225000,270000,300000
Passivo Circulante,400000,450000,500000,550000,600000
Passivo Exigível Total,800000,900000,1000000,1100000,1200000
Dívida Bruta,600000,650000,700000,750000,800000
Caixa e Equivalentes,100000,120000,150000,180000,200000
Patrimônio Líquido,700000,900000,1250000,1600000,1800000
Fluxo de Caixa Operacional,180000,220000,270000,320000,360000
```

**Campos Obrigatórios**:
- Receita Líquida
- EBITDA
- Lucro Líquido
- Ativo Circulante
- Ativo Total
- Estoque
- Passivo Circulante
- Passivo Exigível Total
- Dívida Bruta
- Caixa e Equivalentes
- Patrimônio Líquido
- Fluxo de Caixa Operacional

**Observações Importantes**:
- Os valores podem conter pontos ou vírgulas como separadores decimais
- Símbolos de moeda (R$, $) são automaticamente removidos
- É necessário ter dados de pelo menos 3 anos
- As colunas representam os anos (ex: 2021, 2022, 2023, etc.)

### 2. Fazer Upload do Arquivo

1. Clique em "Browse files" ou arraste o arquivo CSV para a área de upload
2. Opcionalmente, preencha as informações adicionais da empresa (Setor, Faturamento, Número de Funcionários)

### 3. Analisar os Dados

1. Clique no botão "🚀 Analisar Dados Financeiros"
2. Aguarde o processamento

### 4. Interpretar os Resultados

A aplicação apresentará:

- **KPIs do Último Ano**: Cartões com os principais indicadores do período mais recente
- **Gráficos de Evolução**: Visualização da tendência de cada indicador ao longo dos anos
- **Diagnóstico e Plano de Ação**: 
  - Problemas Críticos (🚨): Situações que exigem atenção imediata
  - Alertas (⚠️): Pontos de atenção que devem ser monitorados
  - Soluções Recomendadas: Ações práticas para cada problema identificado

## 📁 Estrutura do Projeto

```
projeto-analise-financeira/
├── .gitignore                      # Arquivos ignorados pelo Git
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── app.py                          # Aplicação principal Streamlit
├── sample_data/
│   └── modelo_balanco_dre.csv     # Modelo de exemplo
├── src/
│   ├── __init__.py
│   ├── data_parser.py             # Leitura e validação de CSV
│   ├── metrics.py                 # Cálculo dos indicadores
│   ├── diagnostics.py             # Motor de diagnóstico
│   └── ui.py                      # Interface Streamlit
└── tests/
    ├── __init__.py
    ├── test_metrics.py            # Testes dos indicadores
    └── test_diagnostics.py        # Testes do diagnóstico
```

## 🔍 Benchmarks Utilizados

O sistema utiliza os seguintes benchmarks de mercado para avaliação:

| Indicador | Crítico | Alerta | Bom |
|-----------|---------|--------|-----|
| Liquidez Corrente | < 1.0 | < 1.5 | ≥ 1.5 |
| Liquidez Seca | < 0.8 | < 1.0 | ≥ 1.0 |
| Endividamento Geral | > 70% | > 50% | ≤ 50% |
| Dívida Líquida/EBITDA | > 4x | > 3x | ≤ 3x |
| Margem EBITDA | < 10% | < 15% | ≥ 15% |
| Margem Líquida | < 0% | < 5% | ≥ 5% |
| ROE | < 0% | < 10% | ≥ 10% |
| FCO/Dívida Total | < 0.1 | < 0.2 | ≥ 0.2 |

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**: Linguagem de programação
- **Streamlit 1.32.0**: Framework web para interface
- **Pandas 2.2.0**: Manipulação de dados
- **Plotly 5.18.0**: Visualização de gráficos interativos
- **Pytest 8.0.0**: Framework de testes

## ❓ Solução de Problemas

### Erro ao importar módulos

Se você encontrar erros como `ModuleNotFoundError`, certifique-se de que:
1. O ambiente virtual está ativado
2. Todas as dependências foram instaladas: `pip install -r requirements.txt`

### Erro ao carregar CSV

Se o CSV não for carregado corretamente:
1. Verifique se todas as contas obrigatórias estão presentes
2. Certifique-se de que há pelo menos 3 anos de dados
3. Verifique se não há caracteres especiais nos nomes das contas
4. Tente salvar o CSV com encoding UTF-8

### Indicadores retornando N/A

Isso pode ocorrer quando:
1. Há divisão por zero (ex: Passivo Circulante = 0)
2. Dados estão faltando no CSV
3. Valores não numéricos estão presentes

## 📚 Conceitos dos Indicadores

### Liquidez Corrente
Mede a capacidade da empresa de pagar suas dívidas de curto prazo com seus ativos circulantes. Valores abaixo de 1.0 indicam que a empresa pode ter dificuldades para honrar compromissos imediatos.

### Liquidez Seca
Similar à Liquidez Corrente, mas exclui os estoques do cálculo, pois nem sempre são facilmente convertíveis em dinheiro.

### Endividamento Geral
Indica o percentual do ativo total financiado por capital de terceiros. Quanto maior, mais endividada está a empresa.

### Dívida Líquida / EBITDA
Mostra quantos anos seriam necessários para pagar todas as dívidas líquidas usando apenas o EBITDA gerado. Valores acima de 3x são preocupantes.

### Margem EBITDA
Indica o percentual da receita que se converte em EBITDA. Mede a eficiência operacional antes de juros, impostos, depreciação e amortização.

### Margem Líquida
Mostra quanto da receita se converte em lucro líquido final. É o indicador de rentabilidade mais importante.

### ROE (Return on Equity)
Mede o retorno sobre o patrimônio líquido. Indica quanto de lucro a empresa gera com o capital próprio investido.

### FCO / Dívida Total
Avalia a capacidade da empresa de gerar caixa operacional em relação às suas dívidas totais.

## 🤝 Contribuindo

Este é um projeto educacional. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é disponibilizado para fins educacionais.

## 📧 Suporte

Para dúvidas ou problemas, consulte a documentação ou abra uma issue no repositório do projeto.

---

**Desenvolvido para análise de saúde financeira empresarial**
