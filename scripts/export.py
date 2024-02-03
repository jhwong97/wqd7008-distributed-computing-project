import requests
import pandas as pd
import re
import os
from bs4 import BeautifulSoup, Tag
from typing import Optional
from dotenv import load_dotenv
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

# Function to extract raw data
def mets_extract(url, 
                payload: Optional[dict] = None,
                headers: Optional[dict] = None):
        
    MAX_RETRIES = 5
    
    # Define the retry strategy
    retry_strategy = Retry(
        total = MAX_RETRIES,
        backoff_factor = 2,
        status_forcelist = [429, 500, 502, 503, 504]
    )
    
    # Create an HTTP adapter with the retry strategy and mount it to session
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Create a new session object
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    retry_attempt = 0 # Initialize retry attempth counter
    
    while retry_attempt <= MAX_RETRIES:
        try:
            print(f'(Attempt: {retry_attempt}) Extracting raw data ... ')
            
            # Make a request using the session object
            raw_data = session.post(url, data = payload, headers = headers, verify=False)    
        
            if raw_data.status_code == 200:
                print('SUCCESS: Raw Data has been extracted')
                raw_data = BeautifulSoup(raw_data.text, 'html.parser') # Parse the HTML
                return raw_data

            else:
                print('FAILED: Raw Data failed to be extracted. Retrying...')

        except Exception as e:
            print(f'(Attempt: {retry_attempt}) An error occured during extration {e}.')        
    
        retry_attempt += 1
    
    print(f'Maximum retries achieved. Extraction process failed. ErrorCode: {raw_data.status_code}.')

    return None

def mets_preprocess(raw_data, dataframe_name, file_path):
    
    result = raw_data.find('table', class_='table-bordered') # Look up for the table
    # Extract table rows
    if not isinstance(result, Tag):
        return
    
    rows = result.find_all('tr')
    
    individual_data = []
    for row in rows:
        data = row.find_all(['th', 'td'])
        if data:
            data = [item.get_text(strip=True) for item in data]
            if 'GRAND TOTAL' not in data:
                individual_data.append(data)
            
    print('Converting raw data to dataframe......')
    # Select a subset of columns from the first row as column names
    df = pd.DataFrame(individual_data[1:], columns=individual_data[0])
    
    # To separate monthly data and yearly data out
    data_month_filter = [col for col in df.columns if '-' not in col or not any(char.isdigit() for char in col)]
    df_monthly = df.loc[:, data_month_filter]
    df_monthly.name = dataframe_name
    df_monthly.to_csv(file_path, index=False)
    print(f'SUCCESS: {dataframe_name} has been created and stored as .csv file')
    return None

def exports_etl(url, 
                dataframe_name, 
                file_path, 
                payload: Optional[dict] = None, 
                headers: Optional[dict] = None):
    try:
        raw_data = mets_extract(url, payload, headers)
        mets_preprocess(raw_data, dataframe_name, file_path)
    except Exception as e:
        print(e)

def mets_transformation(df):
    df = df.transpose().reset_index()
    column_name = list(df.iloc[2,:])
    edited_column_name = []
    for column in column_name:
        column = column.replace(' ', '_').replace('&', '').replace(',','').replace('.','')
        edited_column_name.append(column)
    df = df.iloc[3:]
    df.columns = edited_column_name
    df = df.rename(columns={'PRODUCT_DESCRIPTION': 'date'})

    for column in df.columns:
        if column == 'date':
            df[column] = pd.to_datetime(df[column])
        else:
            df[column] = pd.to_numeric(df[column].str.replace(',', ''))

    df['total_export'] = df.iloc[:,1:].sum(axis=1)
    print(f"SUCCESS: Data Transformation is completed.")
    file_path = "/home/ubuntu/result/export_data_transformed.csv"
    df.to_csv(file_path, index=False)
    print(f"SUCCESS: Transformed Data has been saved.")


load_dotenv()

# Retrieve the csrf_token and Cookie values
csrf_token = os.getenv("csrf_token")
Cookie = os.getenv("cookie")

# URL of targeted site
url = "https://metsonline.dosm.gov.my/tradev2/product-coderesult"

# headers of targeted site
headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "PHPSESSID=938e8fjm1hj9bb07oq3u4fisi4; _csrf=615b79fbeb5a5e5147fee3ac2245a8abb4f3d106b51ba953154dfe4b8036f358a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22V4KGkyVFWmBgtSAZPHpnC8MV4N1-eYuB%22%3B%7D; cookiesession1=678B288423AE9070F6271BFC1DD8DA77"
}

# payload of targeted site
payload = {
    "_csrf": "Q3RsVE1CS1QVQCcTJjsdEhQZLjM5EQoOEzwcOg56BgJ3Ol15KBs.Fg==",
    "Tradev2[typeofsearch]": "classification",
    "Tradev2[typedigit]": 7,
    "Tradev2[rangecode1]": 0,
    "Tradev2[rangecode2]": 9,
    # 'Tradev2[code_idcode]': ,
    # 'Tradev2[code_idcodedigit9]': ,
    # 'Tradev2[tradeflow]': ,
    "Tradev2[tradeflow][]": "exports",
    # 'Tradev2[timeframe]': ,
    "Tradev2[timeframe]": "month",
    # 'Tradev2[rangeyear]': ,
    # 'Tradev2[rangeyear2]': ,
    # 'Tradev2[rangeyearone]': ,
    # 'Tradev2[rangemonthone]': ,
    "Tradev2[mothdata]": 2000,
    "Tradev2[mothdata2]": 2023,
    # 'Tradev2[classification_serch]': ,
    # 'Tradev2[country2]': ,
    "Tradev2[geogroup]": 1,
    "Tradev2[geogroup]": 29,
    "Tradev2[codeshowby]": "code",
}

exports_etl(url, dataframe_name="my_export", file_path="/home/ubuntu/result/export_data.csv", payload=payload, headers=headers)
df = pd.read_csv('/home/ubuntu/result/export_data.csv', sep=",")
mets_transformation(df)