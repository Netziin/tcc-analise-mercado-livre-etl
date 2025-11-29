# 🛒 Análise de Produtos e Tendências de Vendas no Mercado Livre

> **Trabalho de Conclusão de Curso (TCC)** - Centro Universitário UNIFAFIBE

## 📋 Sobre o Projeto

Este projeto é um sistema completo de **Business Intelligence (BI)** desenvolvido para monitorar e analisar o mercado de eletrônicos no Mercado Livre. Ele automatiza a coleta de dados públicos (preços, vendas, marcas), cria um histórico em banco de dados e gera insights estratégicos em dashboards interativos.

### 🚀 Principais Funcionalidades
* **Coleta Automática (ETL):** *Spiders* em Scrapy monitoram diariamente 5 categorias de produtos.
* **Tratamento de Dados:** Scripts em Pandas com Regex limpam dados complexos (ex: conversão de "+10mil vendidos").
* **Histórico de Preços:** Armazenamento em SQL Server para análise temporal.
* **Dashboard Interativo:** Painéis no Power BI com atualização automática via Gateway.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Coleta:** Scrapy Framework
* **Processamento:** Pandas, SQLAlchemy, Regex (`re`)
* **Banco de Dados:** Microsoft SQL Server (2019/2022 Express)
* **Visualização:** Microsoft Power BI (Desktop & Service)
* **Automação:** Windows Task Scheduler & Power BI Gateway

## ⚙️ Como Executar o Projeto

### Pré-requisitos
* Python 3.9 ou superior instalado.
* SQL Server instalado e rodando (Instância `SQLEXPRESS` ou `MSSQLSERVER`).
* Banco de dados `MercadoTCC` criado (ou restaurado via backup).

### Instalação

1. **Clone este repositório** ou baixe os arquivos.
2. **Crie o ambiente virtual:**
   ```bash
   python -m venv .venv