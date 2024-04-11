import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine 
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")

conn_str = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)

def test_read_sql(table_name):
    sql = """
    SELECT * FROM [dbo].table_name
    """
    sql_df = pd.read_sql( sql, con=engine) 
    print(sql_df.head())

def load_data(df, table_name = 'table'):
    try:
        sql_df = df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print("Done")
    except Exception as e:
        print(e)

if __name__ == "__main__":

    # test_read_sql()  
    sample_data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=sample_data)
    load_data(df, 'test_table')
