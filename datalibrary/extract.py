import requests
import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)

BASE_URL = "https://datalib.vam.wfp.org/api/3/"
ENDPOINTS = {
'users': 'action/user_list',
'all_surveys_information': 'action/current_package_list_with_resources',
'all_surveys_code': 'action/package_list',
'member_list': 'action/member_list',
}

class DataLibrary:
    """Class to query WFP Data Library API.

Attributes:
    api_key (str): API key for authentication

Methods:
    get_users: Get list of Data Library users
    get_surveys: Get list of survey codes
    get_survey_info: Get info on all surveys
        """

    def __init__(self, api_key):
        """Initialize DataLibrary instance.

        Args:
        api_key (str): API key for authentication
        """      
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_response(self, url, params=None):
        """Send API request.

        Args:
            url (str): API endpoint URL
            params (dict, optional): Query parameters

        Returns:
            dict: API response
        """
        headers = {'Authorization': f'{self.api_key}'}

        if params is None:
            params = {}
        elif isinstance(params, int):
            params = {'limit': params}

        logger.info(f'Querying {url} with params {params}')

        r = self.session.get(url, headers=headers, params=params)
        if r.status_code == 200:
            response = json.loads(r.content)
            return response
        else:
            logger.error(f"Error {r.status_code} when querying {url}")
            return None

    def help(self):
        """Get basic information on the usage of the API."""
        print(f'\n---\n This library helps RAM users to query the Data Library API:{BASE_URL}\n')
        print('You can get information about the following:')
        for k, v in ENDPOINTS.items():
            info = k.replace("_", " ").capitalize()
            print(f'{info} on endpoint {BASE_URL + v}')

        print("\n---\n For documentation visit: http://docs.ckan.org/en/2.9/api/\n---\n")

    def get_users(self):
        """Get list of users"""
        url = BASE_URL + ENDPOINTS['users']
        response = self.get_response(url) 

        data = response["result"]
        return data

    def get_survey_list(self, limit=None):
        """Get package list"""
        url = BASE_URL + ENDPOINTS['all_surveys_code']
        response = self.get_response(url, params=limit) 
        data = response["result"]
        return data

    def get_surveys_with_resources(self, limit=None):
        """Get all surveys with country, type of survey and description"""
        url = BASE_URL + ENDPOINTS['all_surveys_information']
        response = self.get_response(url, params=limit) 
        data = response["result"]
        return data
    
    def get_member_list(self, id=None, object_type=None, capacity=None, limit=None):
        """Get list of members of a group.

        Args:
            id (str, optional): The ID or name of the group.
            object_type (str, optional): Restrict members to a given type (e.g., 'user' or 'package').
            capacity (str, optional): Restrict members to a given capacity (e.g., 'member', 'editor', 'admin').
            limit (int, optional): Maximum number of results to return.

        Returns:
            list: List of tuples containing (id, type, capacity) for each member.
        """
        url = BASE_URL + ENDPOINTS['member_list']
        params = {'id': id, 'object_type': object_type, 'limit': limit}
        response = self.get_response(url, params=params)
        data = response.get("result", [])
        return data
        
    def __repr__(self):
        return f'DataLibraryData({self.api_key})'

    def __str__(self):
        return f'The API key used in this DataLibraryData is {self.api_key}'


def get_survey_data(client):
  survey_list = client.get_survey_list()
  total_surveys = len(survey_list)

  all_surveys = client.get_surveys_with_resources(limit=total_surveys) 
  all_surveys_df = pd.json_normalize(all_surveys)

  return all_surveys_df


def get_user_data(client):
  users = client.get_users()
  users_df = pd.DataFrame(users)

  return users_df

def get_member_data(client, id=None):
    members = client.get_member_list(id=id)
    members_df = pd.DataFrame(members)
    return members_df


def get_data(client):
  survey_df = get_survey_data(client)
  user_df = get_user_data(client)
  
  result = []
  container_ids = set(survey_df['organization.id'])
  for container_id in container_ids:
    container_members = get_member_data(client, id=container_id)
    if container_members is not None:
        container_members.insert(3, "container_id", container_id) # Check if container_members is not None
        result.append(container_members)
        # BUG: container id should be included as column, along with user_id
  member_df = pd.concat(result, ignore_index=True)

  return survey_df, user_df, member_df


if __name__ == "__main__":
    pass