from dotenv import load_dotenv
import pandas as pd
import os
from etl.extract import DataLibrary
from etl.transform import process_data
from etl.load import load_to_db, save_to_excel


load_dotenv()  # take environment variables from .env.

def extract_data(client):
    """
    Get data from DL api and returns two dataframes.

    This function initializes a DataLibrary API instance, retrieves the survey list and user information from the API, and returns two dataframes - one containing all surveys with resources, and one containing user information.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the dataframes for surveys with resources and users.
    """

    # get survey list in format DATE_ISO3_SURVEYTYPE or DATEISO3SURVEYTYPE
    survey_list = client.get_survey_list()
    # # get total number survey present on Data Library
    total_surveys = len(survey_list)
    
    # get information on user
    users = client.get_users()
    # get total number of users with an account on Data Library
    total_users = len(users)
    users = pd.DataFrame(users)

    print(f"\n---\n There are {total_surveys + 1} surveys and {total_users + 1} active users in Data Library\n---\n ")

    # get all information about surveys
    all_surveys_with_resources = client.get_surveys_with_resources(limit=total_surveys)

    all_surveys_with_resources =  pd.json_normalize(all_surveys_with_resources)

    return  (all_surveys_with_resources, users)

def run_etl_process():
    raw_data = extract_data(DataLibrary(os.getenv("DATALIB_API_KEY")))
    # Load processed data to DB
    processed_data = process_data(raw_data)
    save_to_excel(processed_data)
    load_to_db(processed_data)
    print("Done")

if __name__== "__main__":
    run_etl_process()

