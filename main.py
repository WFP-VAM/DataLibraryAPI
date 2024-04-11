from datalibrary.query_api import DataLibrary
from datalibrary.export_database import load_data
from datalibrary.data_utils import normalize_json, export_to_csv
from dotenv import load_dotenv
import pandas as pd
import os
import logging

load_dotenv()  # take environment variables from .env.

def get_data_from_api():

    # initiate Data Library API instance
    dl = DataLibrary(os.getenv("DATALIB_API_KEY"))

    # call the help function to get basic info about usage
    urls = dl.help()

    # get survey list in format DATE_ISO3_SURVEYTYPE or DATEISO3SURVEYTYPE
    survey_list = dl.get_survey_list()
    # # get total number survey present on Data Library
    total_surveys = len(survey_list)
    
    # get information on user
    users = dl.get_users()
    # get total number of users with an account on Data Library
    total_users = len(users)

    print(f"\n---\n There are {total_surveys + 1} surveys and {total_users + 1} active users in Data Library\n---\n ")

    # get all information about surveys
    all_surveys_with_resources = dl.get_surveys_with_resources(limit=total_surveys)
    all_surveys_with_resources = [normalize_json(item) for item in all_surveys_with_resources]
    
    return  (all_surveys_with_resources, users, survey_list)

def load_data_to_db(processed_data):
    pass
  # Code to load processed data into database

def export_data_to_csv(api_data):
    # export survey list, survey information with resources and user list as csv
    all_filenames = ["datalib_all_info", "datalib_users", "survey_list"]

    for data, filename in zip(api_data, all_filenames):
        export_to_csv(data, filename)



def main():
    """Get user and survey data from Data Library and create CSV files for each of the datasets."""
    api_data = get_data_from_api()
    # export_data_to_csv(api_data)

    all_surveys_with_resources, users, survey_list = api_data

    # load data into database
    print("Loading all surveys info to database")
    load_data(pd.DataFrame(all_surveys_with_resources), 'DL_RawSurveys')
    print("Loading all surveys info to database")

    users = pd.DataFrame(users)
    try:
        load_data(pd.DataFrame(users), 'DL_Users')
    except Exception as e:
        print(f"Error: {e}")

    # Success!
    print("\nAll data saved!")

if __name__== "__main__":
    main()







