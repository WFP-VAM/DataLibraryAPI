from datetime import date
import csv

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

def create_csv(data, filename = "output"):
    """Create CSV file based on data"""

    # Get today's date in format YYY_MM_DD
    today = str(date.today()).replace("-", "_")
    # Create file name with today's date and data
    folder = "output"
    fname = f"{today}_{filename}.csv"
    path = f"{folder}/{fname}"


    if type(data[0]) == str:
        with open(path, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            for survey in data:
                writer.writerow([survey])
    else:
        try: 
            with open(path, 'w', newline="", encoding="utf-8") as csvfile:
                # get row header
                header = list(data[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames = header, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
        except FileNotFoundError:
            print(f"Unable to locate {fname}")

    print(f"{path} saved in {folder}")