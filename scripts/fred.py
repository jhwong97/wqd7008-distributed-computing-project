from fredapi import Fred
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

FRED_API = os.getenv("FRED_API")
fred = Fred(api_key = FRED_API)

def fred_data_extraction(selected_data):
    df_list = []
    for item in selected_data:
        df = fred.get_series_all_releases(item)
        df.name = item
        file_path = f"/home/ubuntu/result/{item}_data.csv"
        df.to_csv(file_path, index=False)
        print(f'SUCCESS: {item} data has been created and stored as .csv file')        

def fred_transformation(csv_name_list):
    for item in csv_name_list:
        csv_file = f"/home/ubuntu/result/{item}_data.csv"
        df = pd.read_csv(csv_file, sep=",")
        df['realtime_start'] = pd.to_datetime(df['realtime_start'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={'value': item})
        file_path = f"/home/ubuntu/result/{item}_data_transformed.csv"
        df.to_csv(file_path, index=False)
        print(f"SUCCESS: {item} data has been transformed and stored as {file_path}.")

selected_data = ['EXMAUS', 'RBMYBIS']
fred_data_extraction(selected_data)
fred_transformation(csv_name_list=selected_data)