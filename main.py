import argparse
import os

from dotenv import load_dotenv

from datalibrary.extract import DataLibrary, get_data, get_all_household_surveys, get_databridges_household_surveys
from datalibrary.load import load_to_db, save_to_excel
from datalibrary.transform import transform

load_dotenv()  # take environment variables from .env.


def main():
    """
    Executes the ETL (Extract, Transform, Load) process to fetch data from VAM Data Library, process the data, and load it into a database and/or save it to an Excel file.

    There are three data points being loaded:
    - Survey Information
    - User Information
    - Survey Resources
    """
    dl_api_data = get_data(DataLibrary(os.getenv("DATALIB_API_KEY")))
    processed_data = transform(dl_api_data)

    db_data = get_databridges_household_surveys()

    processed_data.append(db_data)
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Export Data Library data to CSV or database."
    )
    parser.add_argument("--csv", action="store_true", help="Export data to CSV files")
    parser.add_argument("--db", action="store_true", help="Upload data to a database")
    args = parser.parse_args()

    if args.csv:
        save_to_excel(processed_data)
        print("Data exported to CSV files.")

    if args.db:
        load_to_db(processed_data)
        print("Data uploaded to the database.")

    if not args.csv and not args.db:
        print("No action specified. Use --csv or --db to export data.")


if __name__ == "__main__":
    main()
