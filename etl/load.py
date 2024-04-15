import os
import pandas as pd
from sqlalchemy import create_engine 
from dotenv import load_dotenv
import logging
from datetime import date
from pd_to_mssql import to_sql

logger = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env.

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")

conn_str = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)

class ExcelExportError(Exception):
    pass

def load_data(data, table_name = 'table'):
    try:
        data.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        
        print("Done")
    except Exception as e:
        logger.error(f"Error {e} when populating {table_name}")

def load_to_db(data: tuple, table_names = ("DL_Surveys", "DL_Resources", "DL_Users")):
    try: 
        for df, table_name in zip(data, table_names):
            logger.info("Loading data to database")
            load_data(df, table_name)
    except ExcelExportError as e:
        logger.error(f"Error loading data: {e}")


def save_to_excel(data: tuple, filenames = ("surveys", "resources", "users")):
    # export survey list, survey information with resources and user list as csv
    folder = "output"
    today = str(date.today()).replace("-", "_")


    for df, filename in zip(data, filenames):
        path = f"{folder}/{today}_{filename}.csv"
        try:
            df.to_csv(path)
        except Exception as e:
            logger.error(f"Error saving {filename} to excel")
            continue

if __name__ == "__main__":

    # test_read_sql()  
    sample_data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data=sample_data)
    load_data(df, 'test_table', index=True)
