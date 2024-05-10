import pandas as pd
import json


SURVEY_COLUMNS_SELECTION = ['assessment_status', 'collection_method', 'creator_user_id', 'data_collector', 'description', 'end_date', 'id', 'metadata_created', 'metadata_modified', 'month', 'name', 'num_resources', 'organization_id', 'organization_title', 'organization_description', 'organization_created', 'owner_org', 'private', 'progress_status', 'start_date', 'survey_attributes', 'survey_category', 'survey_type', 'title', 'year', 'resources']

SURVEY_COLUMNS_RENAMING = {"id": "survey_id", "organization_id": "container_id",
                          "organization_title": "container_name",
                          "organization_description": "container_description",
                          "organization_created": "container_created",
                          "data_collector": "organization", "owner_org": "parent_container_id",
                          "title": "survey_title"}

RESOURCES_COLUMNS_TO_DROP = ["resources", "restricted", "restricted-allowed_users", "restricted-level", "cache_last_updated", "cache_url", "revision_id", "url_type", "state", "resource_type", "mimetype_inner", "hash", "package_id"]

def clean_column_names(df):
    """Rename columns to be more readable"""
    df.columns = df.columns.str.replace('.', '_') 
    return df

def flatten_response(df: pd.DataFrame, col: str, _id: str) -> pd.DataFrame:
    flat_list = []
    for _, row in df.iterrows():
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

def user_data_transform(df):
        # Remove unnecessary columns from users table
    users_columns_to_drop = ["apikey", "display_name", "about", "state", "image_url", "image_display_url"]
    df = df.drop(columns=users_columns_to_drop)
    return  df

def survey_data_transform(df):
    df = clean_column_names(df)
    df = df[SURVEY_COLUMNS_SELECTION]
    df = df.rename(columns=SURVEY_COLUMNS_RENAMING)
    return df

def member_data_transform(df):
    df = df.rename(columns={0: "user_id", 1: "type", 2: "capacity"})
    df = df[df.type.isin(["user"])]
    df = df[["user_id", "capacity", "container_id"]]
    return df


def transform(data: tuple) -> tuple:
    """
    Transforms the input data tuple into a new tuple.

    Args:
    data (tuple): A tuple containing the data to be transformed.

    Returns:
    tuple: The transformed data.
    """
    surveys, users, members = data

    surveys = survey_data_transform(surveys)

    # Flatten resources
    resources = surveys[["resources", "container_id", "survey_id"]]
    flat_resources = flatten_response(resources, "resources", "survey_id")

    # Remove unnecessary columns from survey table
    surveys.drop(columns=["resources"], inplace=True) 
    full_resources = pd.merge(resources, flat_resources, on="survey_id")

    # Normalize restricted datasets
    restricted = normalize_restrictions(full_resources)
    full_resources = full_resources.join(restricted)


    # Remove unnecessary columns from resource table
    full_resources.drop(columns=RESOURCES_COLUMNS_TO_DROP, inplace=True)

    # Rename resource columns
    resources_cols_renaming = {
        "level": "access_level",
    }
    full_resources = full_resources.rename(columns=resources_cols_renaming)


    # User table transformations 
    users = user_data_transform(users)

    # Member DF
    members = member_data_transform(members)


    return (surveys, full_resources, users, members)

