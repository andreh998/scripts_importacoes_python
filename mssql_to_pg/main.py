import pandas as pd

from pg_connection import postgres_connect
from mssql_connection import mssql_connect

mssql_engine = mssql_connect()
pg_engine = postgres_connect()

mssql_statement = '''
  select * from emplacamentos
'''

df_mssql = pd.read_sql(
  con=mssql_engine,
  sql=mssql_statement
)

print(df_mssql.head(2))

df_mssql.to_sql(
  con=pg_engine,
  name='emplacamentos',
  if_exists='replace', # ATENÇÃO, O REPLACE DROPA A TABELA ANTES DE INSERIR OS DADOS
  index=False,
  method='multi',
  chunksize=10_000
)
