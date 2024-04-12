from dotenv import load_dotenv
from datetime import date
import pandas as pd
import os
import json
import logging
from datalibrary.query_api import DataLibrary
from datalibrary.export_database import load_data

logger = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env.


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

def export_data_to_csv(data: tuple):
    # export survey list, survey information with resources and user list as csv
    all_filenames = ["surveys", "resources", "users"]
    folder = "output"
    today = str(date.today()).replace("-", "_")

    for df, filename in zip(data, all_filenames):
        path = f"{folder}/{today}_{filename}.csv"
        df.to_csv(path)

def load_to_db(data: tuple):
    table_names = ("DL_Surveys", "DL_Resources", "DL_Users")
    try: 
        for df, table_name in zip(data, table_names):
            logger.info("Loading data to database")
            load_data(df, table_name)
    except Exception as e:
        logger.error(f"Error loading data: {e}")

def process_data(data):
    surveys, users = data
    surveys = surveys[['assessment_status', 'collection_method',
    'creator_user_id', 'data_collector', 'description', 'end_date', 'id',
    'metadata_created', 'metadata_modified', 'month',
    'name', 'num_resources', 'organization.id',
    'organization.title', 'organization.type',
    'organization.description',        'organization.created', 
        'owner_org',
    'private', 'progress_status', 'start_date', 'state',
    'survey_attributes', 'survey_category', 'survey_type', 'title', 'type',
        'year', 'resources']]
    
    surveys.columns = surveys.columns.str.replace('.', '_')
    surveys = surveys.rename(columns={"id": "survey_id"})


    resources = surveys[["resources", "organization_id", "survey_id"]]

    return (surveys, resources, users)


if __name__== "__main__":
    api_data = get_data_from_api()

    # Load processed data to DB
    processed_data = process_data(api_data)
    export_data_to_csv(api_data)


    # Export information to CSV
    # load_to_db(processed_data)

    print("Done")






