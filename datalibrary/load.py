import logging
import os
from datetime import datetime

import pytz
from dotenv import load_dotenv
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)
from sqlalchemy.engine import URL

load_dotenv()  # take environment variables from .env.

DB_HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")


connection_url = URL.create(
    "mssql+pyodbc",
    username=USERNAME,
    password=PASSWORD,
    host=DB_HOST,
    database=DATABASE,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "yes",
        "TrustServerCertificate": "yes",
    },
)
engine = create_engine(
    connection_url
)  # FIXME: executemany would make it faster, but breaks with some data types (dataviz_themes as list?)


class ExcelExportError(Exception):
    pass


def load_data(data, table_name="table"):
    try:
        with engine.connect() as conn:
            data.to_sql(name=table_name, con=conn, if_exists="replace", index=False)
        print(f"Data loaded to {table_name} successfully")

    except (ValueError, TypeError) as e:
        logger.error(f"Error {e} when populating {table_name}")


def load_to_db(
    data: tuple, table_names=("DL_Surveys", "DL_Resources", "DL_Users", "DL_Members", "DB_HHSurveys")
):
    try:
        for df, table_name in zip(data, table_names):
            logger.info("Loading data to database")
            load_data(df, table_name)
    except ExcelExportError as e:
        logger.error(f"Error loading data: {e}")


def save_to_excel(data: tuple, filenames=("surveys", "resources", "users", "members", "household_surveys")):
    # export survey list, survey information with resources and user list as csv
    folder = "output"
    today = datetime.now(pytz.utc).strftime("%Y_%m_%d")

    for df, filename in zip(data, filenames):
        path = f"{folder}/{today}_{filename}.csv"
        try:
            df.to_csv(path)
        except (ValueError, TypeError) as e:
            logger.error(f"Error saving {filename} to excel: {e}")
            continue


if __name__ == "__main__":
    pass
