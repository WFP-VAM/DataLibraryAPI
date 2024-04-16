import pandas as pd
import json


def clean_column_names(df):
    """Rename columns to be more readable"""
    df.columns = df.columns.str.replace('.', '_') 
    return df

def flatten_response(df: pd.DataFrame, col: str, _id: str) -> pd.DataFrame:
    flat_list = []
    for index, row in df.iterrows():
        for r in row[col]:
            flat_dict = {_id : row[_id]} 
            flat_dict.update(r)
            flat_list.append(flat_dict)
            
    df = pd.DataFrame(flat_list)
    return df

def flatten_resources(df):
    resources = df[["resources", "organization_id", "survey_id"]]
    flat_resources = flatten_response(resources, "resources", "survey_id")
    return flat_resources

def normalize_restrictions(df):
    """Normalize restricted column"""
    try:
        df['restricted'] = df['restricted'].apply(json.loads)
    except TypeError:
        pass
    
    restricted = pd.json_normalize(df["restricted"])
    return restricted


def transform(data: tuple) -> tuple:
    surveys, users = data

    # Clean column names
    surveys = clean_column_names(surveys)
    
    # Select relevant columns
    survey_cols = ['assessment_status', 'collection_method', 'creator_user_id', 'data_collector', 'description', 'end_date', 'id', 'metadata_created', 'metadata_modified', 'month', 'name', 'num_resources', 'organization_id', 'organization_title', 'organization_type', 'organization_description', 'organization_created', 'owner_org', 'private', 'progress_status', 'start_date', 'survey_attributes', 'survey_category', 'survey_type', 'title', 'year', 'resources']
                   
    surveys = surveys[survey_cols]
    
    # Rename survey columns
    survey_cols_renaming = {"id": "survey_id", "organization_id": "container_id", "organization_type": "container_type", "organization_title": "container_title", "organization_description": "container_description", "organization_created": "container_created", "data_collector": "organization", "owner_org": "parent_container_id"}
    surveys = surveys.rename(columns= survey_cols_renaming)

    # Flatten resources
    resources = surveys[["resources", "container_id", "survey_id"]]
    flat_resources = flatten_response(resources, "resources", "survey_id")

    # Join back to surveys
    surveys.drop(columns= ['resources'], inplace=True) 
    full_resources = pd.merge(resources, flat_resources, on="survey_id")

    # Normalize restricted datasets
    restricted = normalize_restrictions(full_resources)
    full_resources = full_resources.join(restricted)


    # Drop unnecessary columns
    drop_cols = ["resources", "restricted", "restricted-allowed_users", 
                 "restricted-level", "cache_last_updated", "cache_url", 
                 "revision_id"]
    
    full_resources.drop(columns=drop_cols, inplace=True)

    return (surveys, full_resources, users)

