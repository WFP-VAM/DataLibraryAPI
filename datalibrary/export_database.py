import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

print(os.environ.get("DB_NAME"))

# # Get environment variables
# TABLE_NAME = "CongoCfsvaFullRawResponses"
# USERNAME = os.getenv("HH_USERNAME")
# PWD = os.getenv("HH_PWD")
# HH_SERVER = os.getenv("HH_SERVER")
# HH_DATABASE = os.getenv("HH_DATABASE")

# # Create a connection string with the necessary details
# conn_str = f"mssql+pyodbc://{USERNAME}:{PWD}@{HH_SERVER}/{HH_DATABASE}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no&TrustServerCertificate=yes"

# # Create SQLAlchemy engine
# engine = create_engine(conn_str)
# # Session = sessionmaker(bind=engine)
# # session = Session()

# def get_data_from_source(country_code, survey_id, survey_data):
#     """
#     Retrieves data from a source, either from a pickle file or from DataBridges,
#     and returns it as a pandas DataFrame.

#     Args:
#         country_code (str): The country code.
#         survey_id (str): The survey ID.
#         survey_data (str): The survey data.

#     Returns:
#         pandas.DataFrame: The retrieved data as a pandas DataFrame.
#     """
#     # TEST PURPOSES
#     data = f"static/csfva_congo_{datetime.today().strftime('%Y_%m_%d')}.pkl"

#     if os.path.isfile(data):
#         # Load DataFrame from a pickle file
#         with open(data, 'rb') as f:
#             df = pickle.load(f)
#     else: 
#         # Get the data from DataBridges and store it in a pandas dataframe
#         df = data_bridges.get_data(country_code, survey_id, survey_data)
#         print(f"Data coming from DataBridges has {df.shape}")
        
#         # Convert all float columns to float type
#         float_columns = df.select_dtypes(include=['float64']).columns

#         # Replace invalid values with NaN
#         for col in float_columns:
#             df[col] = pd.to_numeric(df[col], errors='coerce')

#         # Fill NaN values with a default value (e.g., 0)
#         df[float_columns] = df[float_columns].fillna(0)
        
#         # Save DataFrame to a pickle file
#         with open(data, 'wb') as f:
#             pickle.dump(df, f)
#     return df

# def convert_types(df):
#     columns_to_convert = [col for col in df.columns if col.lower().startswith(('fcs', 'rcsi', 'hhexp', 'lcs'))]

#     df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce').apply(np.floor).astype('Int64')

#     return df

# if __name__ == "__main__": 

#     # Set the country and survey codes
#     country_codes = { "COG": 59, "GMT": 103 }
#     survey_codes = { "COG_DEV": 916, "COG_PROD": 3094 }

#     # get data from source
#     df = get_data_from_source(country_codes["COG"], survey_codes["COG_PROD"], "full")
#     print(f"Loading {survey_codes['COG_PROD']} survey that has {df.shape[0]} rows and  {df.shape[1]} columns in {TABLE_NAME}")


#     df = convert_types(df)


#     # df1 = df.head(100) # subset for testing
#     # print(f"Loading d1: {df1.shape}")

    

#     # # Upload data into SQL database using pandas and credentials above
#     # try:
#     #     df1.to_sql(TABLE_NAME, conn_str, if_exists='replace', index=False)
#     # except Exception as e:
#     #     print(e)

#     # print("Done!")


#     size = 100
#     num_chunks = len(df) // size + (1 if len(df) % size != 0 else 0)

#     # Write data to SQL in chunks
#     for i in range(num_chunks):
#         try:
#             df_chunk = df[i*size:(i+1)*size]
#             df_chunk.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
#             print(f"Successfully written chunk {i+1} to SQL. Total records uploaded: {(i+1)*size}")
#         except Exception as e:
#             print(f"An error occurred while writing chunk {i+1} to SQL: {e}")
    
#     print("Done!")