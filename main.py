from dotenv import load_dotenv
import os
from datalibrary.extract import DataLibrary, get_data
from datalibrary.transform import transform
from datalibrary.load import save_to_excel

load_dotenv()  # dtake environment variables from .env.

def main():
    """
    Executes the ETL (Extract, Transform, Load) process to fetch data from VAM Data Library, process the data, and load it into a database and save it to an Excel file.

    There are three data points being loaded:
    - Survey Information
    - User Information
    - Survey Resources
    
    This function is the main entry point for the ETL pipeline. It performs the following steps:
    1. Fetches data from Data Library using the `get_data` function and the `DataLibrary` class, which is configured using an environment variable.
    2. Processes the fetched data using the `process_data` function.
    3. Saves the processed data to an Excel file using the `save_to_excel` function.
    4. Loads the processed data into a database using the `load_to_db` function.
    """
    dl_api_data = get_data(DataLibrary(os.getenv("DATALIB_API_KEY")))
    # Load processed data to DB
    processed_data = transform(dl_api_data)
    save_to_excel(processed_data)

if __name__== "__main__":
    main()
    print("Done")
    

