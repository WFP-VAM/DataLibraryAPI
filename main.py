from config import DATALIB_API_KEY
from datalibrary import datalibrary
from datalibrary.export_excel import normalize_json, create_csv

def main():
    """Get user and survey data from Data Library and create CSV files for each of the datasets."""

    # initiate Data Library API instance
    dl = datalibrary.DataLibrary(DATALIB_API_KEY)

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

    print(f"There are {total_surveys + 1} surveys and {total_users + 1} active users in Data Library")

    # get all information about surveys
    all_surveys_resources = dl.get_all_surveys_information(limit=total_surveys)
    all_surveys = [normalize_json(item) for item in all_surveys_resources]

    # save data as csv
    all_data = [all_surveys, users, survey_list]
    all_filenames = ["datalib_all_info", "datalib_users", "survey_list"]

    for data, filename in zip(all_data, all_filenames):
        create_csv(data, filename)
    
    # Success!
    print("\nAll data saved!")

if __name__== "__main__":
    main()







