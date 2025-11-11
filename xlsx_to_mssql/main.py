import pandas as pd
import re
import os 

from mssql_connection import mssql_connect

# Set options to display all rows and columns for dataframes
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#
## AJUSTAR O NOME DO ARQUIVO E NOME DA ABA DA PLANILHA ##
#
file_name = 'Todas as Intenções de Compra 11-11-2025 11-34-33.xlsx'
sheet = 'Todas as Intenções de Compra'

dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(dir, file_name)

if not os.path.exists(file):
  raise OSError(f'Arquivo não encontrado {file}')

df = pd.read_excel(
  io=file,
  sheet_name=sheet
  ,dtype={'documento': str}
)

# print(df.head(2))

# Ajusta nomes das colunas - lower case, remove espaços do inicio e fim, troca espaços no meio por '_'
for column in df.columns:
  new_col = column.strip().replace(' ', '_').lower()
  df = df.rename(columns={column: new_col})

# print(df.head(2))

# Se tiver uma coluna com cpf/cnpj e não for NAN, remove traços, pontos, barras e espaços
df['documento_(br:_cpf/cnpj)_(conta)_(conta)'] = df['documento_(br:_cpf/cnpj)_(conta)_(conta)'].apply(
  lambda x: re.sub(r'[/\.-]', '', x).strip() if pd.notnull(x) else ''
).astype(str)

# print(df.head(2))

# transforma a coluna alterando seu valor
# df['tipo'] = df['tipo'].apply(
#   lambda x: x.replace('(BR)', '').strip() if pd.notnull(x) else ''
# ).astype(str)

# print(df.head(2))

# Se tiver oclunas pra remover
df.drop(columns=[
  '(não_modificar)_oportunidade', 
  '(não_modificar)_soma_de_verificação_da_linha', 
  '(não_modificar)_data_de_modificação'
  ], inplace=True)

# print(df.head(2))
# print(df.columns)

# Renomeia colunas se necessário
df.rename(columns={
  'data_de_criação': 'data_criacao_intencao',
  'conta': 'cliente',
  'documento_(br:_cpf/cnpj)_(conta)_(conta)': 'cpf_cnpj',
  'vendedor_(conta)_(conta)': 'vendedor',
  'concessionária_(conta)_(conta)': 'concessionaria',
  'fase_do_negócio': 'fase_negocio',
  'previsão_de_compra': 'previsao_de_compra',
  'data_de_previsão_do_faturamento': 'data_previsao', 
  'razão_do_status': 'razao_status',
  'término_da_vigência': 'termino_vigencia', 
  'data_de_modificação': 'data_modificacao'
}, inplace=True)

df.drop(columns=['id_cliente_demonstração'], inplace=True)

# print(df.head(2))

mssql_engine = mssql_connect()

df.to_sql(
  con=mssql_engine,
  name='intencoes_crm',
  if_exists='replace', # ATENÇÃO, O REPLACE DROPA A TABELA ANTES DE INSERIR OS DADOS
  index=True, # adiciona código
  index_label='id', # cria uma coluna desse nome com o código
  method='multi',
  chunksize=100 # POR ALGUM MOTIVO USAR CHUNKSIZE MAIOR QUE 100 ESTÁ RETORNANDO ERRO NO MSSQL
)
