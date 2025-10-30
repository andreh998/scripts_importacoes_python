from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def postgres_connect():  
  server = os.getenv('POSTGRES_SERVER')
  database = os.getenv('POSTGRES_DATABASE')
  username = os.getenv('POSTGRES_USER')
  password = os.getenv('POSTGRES_PASS')

  ENCODED_PASSWORD = quote_plus(password)

  connection_string = f'postgresql+psycopg2://{username}:{ENCODED_PASSWORD}@{server}:5432/{database}'

  engine = create_engine(connection_string)

  return engine