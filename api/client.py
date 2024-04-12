import requests
import json
import pandas as pd 
import logging 


logger = logging.getLogger(__name__)

BASE_URL = "https://datalib.vam.wfp.org/api/3/"
ENDPOINTS = {
'users': 'action/user_list',
'all_surveys_information': 'action/current_package_list_with_resources',
'all_surveys_code': 'action/package_list'
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
    
    def get_response(self, url, limit=None):
        """Send API request.

        Args:
            url (str): API endpoint URL
            limit (int, optional): Max number of results
        
        Returns:
            dict: API response 
        """
        headers = { 'Authorization': f'{self.api_key}'}
        params = {'limit': limit}

        logger.info(f'Querying {url} with limit {limit}')

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
        response = self.get_response(url, limit=limit) 
        data = response["result"]
        return data

    def get_surveys_with_resources(self, limit=None):
        """Get all surveys with country, type of survey and description"""
        url = BASE_URL + ENDPOINTS['all_surveys_information']
        response = self.get_response(url, limit=limit) 
        data = response["result"]
        return data

    def __repr__(self):
        return f'DataLibraryData({self.api_key})'

    def __str__(self):
        return f'The API key used in this DataLibraryData is {self.api_key}'

        
