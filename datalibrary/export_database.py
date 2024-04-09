import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

def test_connection():
    # sample data
    sample_data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df = pd.DataFrame(sample_data)
    sql = """
    SELECT * FROM [dbo].IpcValues
    """
    try:
        conn = pyodbc.connect(conn_str)
        # cursor = conn.cursor()
        # cursor.execute(sql)

        # cursor.close()
        # conn.close()

        data = pd.read_sql(sql,conn) 
        print(data.head())
    except Exception as e:
        print(e)



if __name__ == "__main__":


    load_dotenv()  # take environment variables from .env.

    SERVER = os.getenv("SERVER")
    DATABASE = os.getenv("DB_NAME")
    USERNAME = os.getenv("DB_USERNAME")
    PASSWORD = os.getenv("DB_PASSWORD")

    conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

    test_connection()

