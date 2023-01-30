# Data Library API tool

This is a simple Python tool to get data from the [RAM Data Library API]((https://datalib.vam.wfp.org)) in CSV format.

Currently this tools query three API endpoints: 
- **```user_list```**: Get list of users registered in Data Library
- **```package_list```**: Get survey codes (YYMM_ISO3_SURVEYTYPE) for all surveys available in the platform
- ***```current_package_list_with_resources```**: Complete information about surveys in Data Library, including name of survey, survey code, country and uploader

For more information on the RAM Data Library API, consult the [documentation](https://docs.ckan.org/en/2.9/api/) 

## How to use it

1. Make sure you have Python installed on your machine. 
2. Get an API key from your [Data Library](https://datalib.vam.wfp.org) account
3. Add your API key to the api_key.py file. Do not forget to add this file to the .gitignore!
4. Run main.py

>> **Quick tip**
>> 
>> If you're stuck, use the help() function in the DataLibraryData class for information about usage
>>