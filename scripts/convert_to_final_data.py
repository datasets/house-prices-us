import os
import csv

from datetime import datetime

data = 'data/'
archive = 'archive/'
header_order = [
    'AZ-Phoenix', 'CA-Los Angeles', 'CA-San Diego', 'CA-San Francisco', 'CO-Denver', 
    'DC-Washington','FL-Miami', 'FL-Tampa', 'GA-Atlanta', 'IL-Chicago', 'MA-Boston', 'MI-Detroit', 
    'MN-Minneapolis', 'NC-Charlotte', 'NV-Las Vegas', 'NY-New York', 'OH-Cleveland', 'OR-Portland', 
    'TX-Dallas', 'WA-Seattle', 'Composite-10', 'Composite-20', 'National-US'
]

file_key_map = {
    'Phoenix': 'AZ-Phoenix',
    'Los Angeles': 'CA-Los Angeles',
    'San Diego': 'CA-San Diego',
    'San Francisco': 'CA-San Francisco',
    'Denver': 'CO-Denver',
    'Washington': 'DC-Washington',
    'Miami': 'FL-Miami',
    'Tampa': 'FL-Tampa',
    'Atlanta': 'GA-Atlanta',
    'Chicago': 'IL-Chicago',
    'Boston': 'MA-Boston',
    'Detroit': 'MI-Detroit',
    'Minneapolis': 'MN-Minneapolis',
    'Charlotte': 'NC-Charlotte',
    'Las Vegas': 'NV-Las Vegas',
    'New York': 'NY-New York',
    'Cleveland': 'OH-Cleveland',
    'Portland': 'OR-Portland',
    'Dallas': 'TX-Dallas',
    'Seattle': 'WA-Seattle',
    '10-City Composite': 'Composite-10',
    '20-City Composite': 'Composite-20',
    'U.S. National': 'National-US'
}

def get_key_from_filename(filename):
    for key in file_key_map:
        if key in filename:
            return file_key_map[key]
    return None

def cities_month_csv(season):
    file_name = ''.join(['data/', 'cities-month', season, '.csv'])
    start_time = datetime(1987, 1, 1)

    season_files = [f for f in os.listdir(archive) if season in f]
    sorted_files = sorted(season_files, key=lambda x: header_order.index(get_key_from_filename(x)))

    # Load every archive file into a {date_str: value} dict
    series_data = {}
    for file in sorted_files:
        with open(archive + file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            series_data[file] = {row[0]: row[1] for row in reader}

    # Use the national archive file to define the authoritative date sequence
    national_file = next(f for f in sorted_files if 'national' in f.lower())
    date = sorted(
        d for d in series_data[national_file]
        if datetime.strptime(d, "%Y-%m-%d") >= start_time
    )

    # Align every series to the date sequence; blank-fill months before a series begins
    final_list = [[series_data[f].get(d, '') for d in date] for f in sorted_files]

    with open(file_name, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Date'] + header_order)
        writer.writerows(zip(date, *final_list))
    
                            
def national_month_csv():
    """
        Create a csv file with the data
        :param data: dict
        :return: None
    """
    file_name = ''.join([data, 'national-month.csv'])
    print(f"Creating the csv file: {file_name}")
    date = []
    sa = []
    nsa = []
    dir_list = os.listdir(archive)
    header = ['Date','National-US','National-US-SA']
    for elem in dir_list:
        if '-SA' in elem and 'national' in elem.lower():
            with open(archive + elem, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    date.append(row[0])
                    sa.append(row[1])
        elif '-NSA' in elem and 'national' in elem.lower():
            with open(archive + elem, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    nsa.append(row[1])
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for (i, j, k) in zip(date, sa, nsa):
            writer.writerow([i, j, k])
    print(f"File created: {file_name}")

def process():
    national_month_csv()
    cities_month_csv('-SA')
    cities_month_csv('-NSA')

if __name__ == '__main__':
    process()