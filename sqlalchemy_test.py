import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine 
from dotenv import load_dotenv

def test_read_sql():
    sql = """
    SELECT * FROM [dbo].IpcValues
    """
    sql_df = pd.read_sql( sql, con=engine) 
    print(sql_df.head())

def test_write_sql():
    # sample data
    sample_data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c'], 'col3': ['d', 'e', 'f']}
    df = pd.DataFrame(sample_data)
    try:
        sql_df = df.to_sql(name='DL_test', con=engine, if_exists='replace', index=False)
        print("Done")
    except Exception as e:
        print(e)


if __name__ == "__main__":


    load_dotenv()  # take environment variables from .env.

    SERVER = os.getenv("SERVER")
    DATABASE = os.getenv("DB_NAME")
    USERNAME = os.getenv("DB_USERNAME")
    PASSWORD = os.getenv("DB_PASSWORD")

    conn_str = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(conn_str)

    # test_read_sql()
    test_write_sql()


    

