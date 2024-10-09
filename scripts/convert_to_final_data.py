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
    """
        Create a csv file with the data
        :param data: dict
        :return: None
    """
    file_name = ''.join(['data/', 'cities-month', season, '.csv'])
    dir_list = os.listdir(archive)
    start_time = datetime(1987, 1, 1)
    sorted_files = sorted(dir_list, key=lambda x: header_order.index(get_key_from_filename(x)))
    #print(sorted_files)
    with open(file_name, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        final_list = []
        date = []
        # Iterate over each CSV file
        for i, file in enumerate(dir_list):
            if season in file:
                temp = []
                if 'national' in file.lower():
                    with open(archive + file, 'r') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            row_date = datetime.strptime(row[0], "%Y-%m-%d")
                            if row_date >= start_time:
                                date.append(row[0])
                                temp.append(row[1])
                            else:
                                temp.append('')   
                    final_list.append(temp)
                else:  
                    with open(archive + file, 'r') as f:
                        reader = csv.reader(f)
                        next(reader)
                        for row in reader:
                            row_date = datetime.strptime(row[0], "%Y-%m-%d")
                            if row_date >= start_time:
                                temp.append(row[1])
                            else:
                                temp.append('')   
                    final_list.append(temp)
        writer.writerow(['Date'] + header_order)
        writer.writerows(zip(date, *final_list))
    ## Add date to the csv file
    
                            
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