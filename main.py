from dotenv import load_dotenv
import pandas as pd
import os
from api.client import DataLibrary
from scripts.utils import process_data
from scripts.export import load_to_db, save_to_excel


load_dotenv()  # dtake environment variables from .env.

def get_data_from_api():
    """
    Get data from DL api and returns two dataframes.

    This function initializes a DataLibrary API instance, retrieves the survey list and user information from the API, and returns two dataframes - one containing all surveys with resources, and one containing user information.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the dataframes for surveys with resources and users.
    """
    # initiate Data Library API instance
    dl = DataLibrary(os.getenv("DATALIB_API_KEY"))

    # get survey list in format DATE_ISO3_SURVEYTYPE or DATEISO3SURVEYTYPE
    survey_list = dl.get_survey_list()
    # # get total number survey present on Data Library
    total_surveys = len(survey_list)
    
    # get information on user
    users = dl.get_users()
    # get total number of users with an account on Data Library
    total_users = len(users)
    users = pd.DataFrame(users)

    print(f"\n---\n There are {total_surveys + 1} surveys and {total_users + 1} active users in Data Library\n---\n ")

    # get all information about surveys
    all_surveys_with_resources = dl.get_surveys_with_resources(limit=total_surveys)

    all_surveys_with_resources =  pd.json_normalize(all_surveys_with_resources)

    return  (all_surveys_with_resources, users)



if __name__== "__main__":
    api_data = get_data_from_api()
    # Load processed data to DB
    processed_data = process_data(api_data)
    save_to_excel(processed_data)
    print("Done")






