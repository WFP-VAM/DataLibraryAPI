# Data Library API Tool
This is a Python CLI tool to query the [WFP Data Library API](https://datalib.vam.wfp.org/) and export the data into CSV files or an MS SQL database. It performs an ETL (Extract, Transform, Load) process to fetch data from the VAM Data Library, process the data, and load it into a database and/or save it to an Excel file.

## Features
- Queries the Data Library API to get information about users, surveys, resources, and container members.
- Exports data to CSV files.
- Uploads data to an MS SQL database.

## Usage
1. Clone this repository.
2. Get an API key from your Data Library account.
3. Rename the `.env-example` file to `.env`.
4. Add the API key and database credentials to the `.env` file.
5. Run `python main.py` to query the API and export data.
6. Use the `--csv` flag to export data to CSV files (e.g., `python main.py --csv`).
7. Use the `--db` flag to upload data to a database (e.g., `python main.py --db`).
8. The output CSV files will be saved in the `output` folder.

## Requirements
- Python 3.x
- Packages listed in `requirements.txt`

## Documentation
For more details on the Data Library API endpoints, see the [API documentation](http://docs.ckan.org/en/2.9/api/).

## Contributing
Contributions to add more API querying/exporting functionality are welcome!

## License
This project is licensed under the Affero GPL License - see the [LICENSE](LICENSE) file for details.
