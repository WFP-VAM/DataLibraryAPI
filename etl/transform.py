import pandas as pd
import json

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

def flatten_response(df, col: str, df_id: str):
    flat_list = []
    for index, row in df.iterrows():
        for r in row[col]:
            flat_dict = {df_id : row[df_id]} 
            flat_dict.update(r)
            flat_list.append(flat_dict)
            
    df1 = pd.DataFrame(flat_list)
    return df1

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

    resources_df = flatten_response(resources, "resources", "survey_id")
    full_resources = pd.merge(resources, resources_df, on="survey_id")
    
    # restricted resources
    try:
        full_resources['restricted'] = full_resources['restricted'].apply(json.loads)
    except TypeError:
        pass

    restricted = pd.json_normalize(full_resources["restricted"])
    full_resources = full_resources.join(restricted)
    full_resources = full_resources.drop(columns=["resources", "restricted",  "restricted-allowed_users", "restricted-level", 'cache_last_updated', 'cache_url', "revision_id"])

    return (surveys, full_resources, users)

