"""
    This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.
"""

import os
import csv
import json
import time
import requests
import pandas as pd

from bs4 import BeautifulSoup

data = 'archive/'
realtime_start = '1987-01-01'
realtime_end = '2024-10-08'
source = 'https://api.stlouisfed.org/fred/series/observations?series_id='

api_key = os.environ['API_KEY'] ## YOUR API KEY

season_price_index = {
    '-SA': 'https://fred.stlouisfed.org/release/tables?rid=199&eid=243552',
    '-NSA': 'https://fred.stlouisfed.org/release/tables?rid=199&eid=243576'
}

def custom_round(value):
    # Check if the value is numeric (float)
    if isinstance(value, float):
        # Round the value to 3 decimal places
        rounded_value = round(value, 3)
        # Ensure that the formatted string keeps up to 3 decimal places
        return "{:.3f}".format(rounded_value)
    return value

def get_indexes_list(house_price_index):
    """
        Get the list of indexes from the given url
        :param url: str
        :return: dict
    """
    dct = {
        'values': [],
    }
    header_names = {
        'names': []
    }
    try:
        response = requests.get(house_price_index)
        if response.status_code != 200:
            print(f"Failed to get the page with status code: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        get_span = soup.find_all('span',{'class':'fred-rls-elm-nm'})
        for elem in get_span:
            if '/series' in elem.find('a').get('href'):
                dct['values'].append(elem.find('a').get('href'))
                header_names['names'].append(elem.text)
    except requests.exceptions.Timeout:
        print("The server didn't respond. Please, try again later.")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Please, try again later.")
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return dct, header_names

def run_api(series_id):
    """
        Run the api to get the data
        :param series_id: str
        :return: dict
    """
    series_id = series_id.split('/')[-1]
    response = requests.get( 
                            source + series_id +  \
                            '&api_key=' + api_key + '&file_type=json&realtime_start=' + \
                            realtime_start + '&realtime_end=' + realtime_end
                           )
    if response.status_code != 200:
        print(f"Failed to get the page with status code: {response.status_code}")
        return
    data = response.json()
    return data

def create_csv(json_data, header_file_name, season):
    """
        Create a csv file with the data
        :param data: dict
        :return: None
    """
    file_name = ''.join(data + header_file_name + season + '.csv')
    print(f"Creating the csv file: {file_name}")
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Indicator'])
        for elem in json_data['observations']:
            writer.writerow([elem['date'], elem['value']])
    print(f"File created: {file_name}")

import pandas as pd

def clean_vintage_data_dynamic(df, file_name, season):
    """
    Cleans the DataFrame by removing duplicates for two periods:
    1. Before the last 'dot' (".") value: Retains only the latest vintage (ignores empty or null indicators).
    2. After the last 'dot' value: Keeps the latest entry for each date.
    
    :param df: DataFrame containing 'Date' and 'Indicator' columns.
    :param file_name: The name of the file for saving.
    :param season: Additional suffix for the file name.
    :return: Cleaned DataFrame
    """
    print(f"Cleaning the data for {file_name}")
    
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Check for the last occurrence of "." in the 'Indicator' column
    last_dot_index = df[df['Indicator'] == "."].index.max() if "." in df['Indicator'].values else None

    if pd.isna(last_dot_index) or last_dot_index is None:
        # If there is no dot value, handle the whole dataframe as post-dot period
        pre_dot_df = pd.DataFrame()  # Empty pre-dot DataFrame
        post_dot_df = df
    else:
        # Split the dataframe into pre-dot and post-dot periods
        pre_dot_df = df.loc[:last_dot_index]
        post_dot_df = df.loc[last_dot_index + 1:]

    # For pre-dot data: remove rows where 'Indicator' is None or "."
    if not pre_dot_df.empty:
        pre_dot_cleaned = pre_dot_df.dropna(subset=['Indicator'])
        pre_dot_cleaned = pre_dot_cleaned[pre_dot_cleaned['Indicator'] != "."]
        # Drop duplicates for pre-dot data, keeping the latest
        pre_dot_dedup = pre_dot_cleaned.drop_duplicates(subset=['Date'], keep='last')
    else:
        pre_dot_dedup = pd.DataFrame()

    # For post-dot data: drop duplicates and keep the latest one
    post_dot_dedup = post_dot_df.drop_duplicates(subset=['Date'], keep='last')

    # Combine both periods back into one DataFrame
    cleaned_df = pd.concat([pre_dot_dedup, post_dot_dedup])

    # Sort by date to maintain order
    cleaned_df = cleaned_df.sort_values(by='Date')

    # Convert 'Indicator' column to numeric (this will handle any non-numeric values like ".")
    cleaned_df['Indicator'] = pd.to_numeric(cleaned_df['Indicator'], errors='coerce')

    # Round values in the 'Indicator' column using custom_round function
    cleaned_df['Indicator'] = cleaned_df['Indicator'].apply(custom_round)

    # Save the cleaned DataFrame to a CSV file
    file_path = data + file_name + season + '.csv'
    cleaned_df.to_csv(file_path, index=False)
    
    print(f"Data updated and cleaned to {file_path}")
    return cleaned_df


def process():
    print("Processing the data for house price index")
    start = time.time()
    for season, index_price in season_price_index.items():
        links, header_names = get_indexes_list(index_price)  
        if links:
            for (key1, value1), (key2, value2) in zip(links.items(), header_names.items()):
                time.sleep(10) # Delay between seasonal and non seasonal adjusted data
                for (link1, file_name) in zip(value1, value2):
                    json_data = run_api(link1)
                    if json_data:
                        create_csv(json_data, file_name, season)
                        df = pd.read_csv(data + file_name + season + '.csv')
                        clean_vintage_data_dynamic(df, file_name, season)
                        time.sleep(5) # Delay between each request to FRED API
                    else:
                        print(f"No data found for this index {link1}")
        else:
            print("No links found")
            return
    end = time.time()
    print(f"Processing completed in {end-start} seconds")

if __name__ == '__main__':
    process()