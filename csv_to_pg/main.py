import os
import pandas as pd
import re
# precisa instalar o openpyxl pra ler do excel -- pip3 install openpyxl

from pg_connection import postgres_connect

#
## AJUSTAR O NOME DO ARQUIVO ##
#
file_name = 'vendas.csv'

dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(dir, file_name)

if not os.path.exists(file):
  raise OSError(f'Arquivo não encontrado {file}')

df = pd.read_csv(
  filepath_or_buffer=file,
  sep=',',
  header=0,
  decimal='.',
  encoding='utf-8',
  dtype={'cg_cgccpf': str}
)

# print(df.head(2))

# Ajusta nomes das colunas - lower case, remove espaços do inicio e fim, troca espaços no meio por '_'
for column in df.columns:
  new_col = column.strip().replace(' ', '_').lower()
  df = df.rename(columns={column: new_col})

# print(df.head(2))

# Se tiver uma coluna com cpf/cnpj e não for NAN, remove traços, pontos, barras e espaços
df['cg_cgccpf'] = df['cg_cgccpf'].apply(
  lambda x: re.sub(r'[/\.-]', '', x).strip() if pd.notnull(x) else ''
).astype(str)

# print(df.head(2))

# Se tiver oclunas pra remover
df.drop(columns=['conta', 'soma', 'data_mod'], inplace=True)

# print(df.head(2))

engine = postgres_connect()

df.to_sql(
  con=engine,
  name='temp_vendas_data',
  if_exists='replace', # ATENÇÃO, O REPLACE DROPA A TABELA ANTES DE INSERIR OS DADOS
  index=False,
  method='multi',
  chunksize=10_000
)