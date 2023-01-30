import requests
import json

BASE_URL = "https://datalib.vam.wfp.org/api/3/"
ENDPOINTS = {
'users': 'action/user_list',
'all_surveys_information': 'action/current_package_list_with_resources',
'all_surveys_code': 'action/package_list'
}

class DataLibraryData:

    def __init__(self, api_key):
        """Intitialize Data Library class to query API.

        Args:
            api_key (str): API Key to 
        """
        self.api_key = api_key
    
    def get_response(self, url, limit=None):
        """Utility function to query the Data Library API: https://datalib.vam.wfp.org/api/3".

        Args:
            url (str): WFP Data Library endpoint
            limit (int, optional):  if given, the list of datasets will be broken into pages of at most limit datasets per page and only one page will be returned at a time (optional). Defaults to None.

        Returns:
            dict: Raw API response
        """
        headers = { 'Authorization': f'{self.api_key}'}
        params = {'limit': limit}
        r = requests.get(url, headers=headers, params=params)
        if r.status_code == 200:
            response = json.loads(r.content)
            return response
        else:
            print("Error - status code is %s" % r.status_code)
            return None

    def help(self):
        """Get basic information on the usage of the API."""
        print(f'This library helps RAM users to query the Data Library API:{BASE_URL}\n')
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

    def get_all_surveys_information(self, limit=None):
        """Get all surveys with country, type of survey and description"""
        url = BASE_URL + ENDPOINTS['all_surveys_information']
        response = self.get_response(url, limit=limit) 
        data = response["result"]
        return data

    def __repr__(self):
        return f'DataLibraryData({self.api_key})'

    def __str__(self):
        return f'The API key used in this DataLibraryData is {self.api_key}'

        
