import os
import csv
import urllib
import shutil
import dataconverters

url_national = 'http://us.spindices.com/documents/additionalinfo/20131126/64929_csnational-values-1126.xls'
url_cities = 'http://us.spindices.com/documents/additionalinfo/20131126/64929_cshomeprice-history-1126.xls'
xls_national = 'tmp/national.xls'
xls_cities = 'tmp/cities.xls'
tmp_national = 'tmp/national.csv'
tmp_cities = 'tmp/cities.csv'
out_national_year = 'data/national-year.csv'
out_national_quarter = 'data/national-quarter.csv'
out_cities = 'data/cities-month.csv'

def setup():
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if not os.path.exists('data'):
        os.makedirs('data')

def retrieve():
    urllib.urlretrieve(url_national, xls_national)
    urllib.urlretrieve(url_cities, xls_cities)

def xls_to_csv():
    dataconverters.dataconvert(xls_national, tmp_national)
    dataconverters.dataconvert(xls_cities, tmp_cities, guess_types=False)

def process_national():
    fo = open(tmp_national)
    reader = csv.DictReader(fo)
    foout = open(out_national_year, 'w')
    writer = csv.writer(foout)
    writer.writerow(['Year', 'Composite-US'])
    vals = []
    for row in reader:
        year = row['YEAR'][:4]
        quarter = row['QTR'][1]
        vals.append(float(row['COMPOSITE-US']))
        if quarter == '4':
            val = round(sum(vals) / 4, 2)
            vals = []
            writer.writerow([year, val])

def process_national_q():
    fo = open(tmp_national)
    reader = csv.DictReader(fo)
    foout = open(out_national_quarter, 'w')
    writer = csv.writer(foout)
    writer.writerow(['Date', 'Composite-US'])
    for row in reader:
        year = row['YEAR'][:4]
        date = '%s-%02d-01' % (year, (int(row['QTR'][1])-1)*3+1)
        writer.writerow([date, row['COMPOSITE-US']])

def process_cities():
    indata = open(tmp_cities).read()
    # fix time in dataconvert which adds 00:00:00
    indata = indata.replace(' 00:00:00', '')
    indata = indata.replace('column_1', 'Date')
    indata = indata.split('\n')
    del indata[1]
    indata = '\n'.join(indata)
    open(out_cities, 'w').write(indata)

def process():
    setup()
    retrieve()
    xls_to_csv()
    process_national()
    process_national_q()
    process_cities()

if __name__ == '__main__':
    process()

