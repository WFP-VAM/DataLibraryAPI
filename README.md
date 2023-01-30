# Data Library API tool

This is a simple Python tool to query the [RAM Data Library API]((https://datalib.vam.wfp.org)) on three key endpoints:
- Users: Get user list
- Survey List: Get survey list in format YYMM_ISO3_SURVEYTYPE
- Survey List with Resources: Complete information about surveys in Data Library

## How to use it

1. Make sure you have Python installed on your machine. 
2. Get an API key from your [Data Library](https://datalib.vam.wfp.org) account
3. Add your API key to the api_key.py file. Do not forget to add this file to the .gitignore!
4. Run main.py

>> **Quick tip**
>> 
>> If you're stuck, use the help() function in the DataLibraryData class for information about usage
>>