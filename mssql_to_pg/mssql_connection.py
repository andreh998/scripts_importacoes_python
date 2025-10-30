from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def mssql_connect():
  server = os.getenv('MSSQL_SERVER')
  port = os.getenv('MSSQL_PORT')
  database = os.getenv('MSSQL_DATABASE')
  username = os.getenv('MSSQL_USER')
  password = os.getenv('MSSQL_PASS')
  driver = os.getenv('MSSQL_DRIVER')

  connection_string = f'mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver={driver}&TrustServerCertificate=yes'

  engine = create_engine(connection_string)

  return engine