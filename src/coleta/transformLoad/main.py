import pandas as pd
from pathlib import Path
from datetime import datetime
import re
from sqlalchemy import create_engine



script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent
data_folder = project_root / "data"
jsonl_files = list(data_folder.glob("*.jsonl"))

df = None

if not jsonl_files:
    print(f"ERRO CRÍTICO: Nenhum arquivo .jsonl encontrado na pasta '{data_folder}'.")
    print("Execute os spiders primeiro para gerar os arquivos de dados.")
    exit()

try:
    print(f"Encontrados {len(jsonl_files)} arquivos para processar: {[f.name for f in jsonl_files]}")
    
    df_list = [pd.read_json(file, lines=True) for file in jsonl_files]
    df = pd.concat(df_list, ignore_index=True)

    if df.empty:
        print("Aviso: Os arquivos .jsonl estão vazios ou não contêm dados válidos.")
    else:
        print(f"Arquivos lidos e combinados com sucesso. Total de {len(df)} linhas carregadas.")

except Exception as e:
    print(f"ERRO CRÍTICO inesperado ao ler ou processar os arquivos .jsonl: {e}")
    exit()

if df is None or df.empty:
    print("Nenhum dado para processar. Encerrando o script.")
    exit()

pd.options.display.max_columns = None



df['_datetime'] = datetime.now()


print("Iniciando limpeza e transformação dos dados...")

def parse_reviews_amount(text):
    if not text or not isinstance(text, str):
        return 0
    text = text.lower().strip()
    match = re.search(r'(\d+(?:[\.,]?\d*)?)\s*(mil)?', text)
    if not match:
        return 0
    number = match.group(1).replace('.', '').replace(',', '.')
    try:
        number = float(number)
    except:
        return 0
    if match.group(2): 
        number *= 1000
    return int(number)


def limpa_preco(valor):
    if pd.isna(valor):
        return 0
    valor = str(valor).replace('.', '').replace(',', '.').strip()
    valor_numerico = pd.to_numeric(valor, errors='coerce')
    return valor_numerico if not pd.isna(valor_numerico) else 0

df['reviews_rating_number'] = pd.to_numeric(df['reviews_rating_number'], errors='coerce')
df['reviews_amount'] = df['reviews_amount'].apply(parse_reviews_amount)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex=False)
df['new_money'] = pd.to_numeric(df['new_money'], errors='coerce')
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex=False)
df['old_money'] = pd.to_numeric(df['old_money'], errors='coerce')

print("Limpeza e transformação dos dados concluídas.")


server_name = '127.0.0.1,1433'
database_name = 'MercadoTCC'      
driver_name = 'ODBC Driver 17 for SQL Server' 
conn_str = f'mssql+pyodbc://{server_name}/{database_name}?driver={driver_name.replace(" ", "+")}&trusted_connection=yes&TrustServerCertificate=yes'

try:
    print(f"\nTentando conectar ao SQL Server: Servidor='{server_name}', Banco='{database_name}'...")
    engine = create_engine(conn_str)

  
    table_name = 'produtos'
    print(f"Salvando dados na tabela '{table_name}'...")
    df.to_sql(table_name, engine, if_exists='append', index=False)

    print(f"\nDados salvos com sucesso na tabela '{table_name}' do banco '{database_name}'.")
    print("\nPrimeiras 5 linhas do DataFrame combinado que foi salvo:")
    print(df.head())

except Exception as e:
    print(f"\nERRO CRÍTICO ao conectar ou salvar os dados no SQL Server: {e}")
   