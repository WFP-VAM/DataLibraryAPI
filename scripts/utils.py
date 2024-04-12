import pandas as pd


def normalize_json(data: dict) -> dict:
    """Flatten json"""
    new_data = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            new_data[key] = value
        else:
            for k, v in value.items():
                new_data[key + "_" + k] = v
  
    return new_data

def process_data(data: tuple) -> tuple:
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
    surveys.drop('resources', axis=1)

    return (surveys, resources, users)