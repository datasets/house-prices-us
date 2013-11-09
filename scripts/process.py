import csv

def process_national():
    fo = open('cache/national.csv')
    reader = csv.DictReader(fo)
    foout = open('data/national-yearly.csv', 'w')
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
    fo = open('cache/national.csv')
    reader = csv.DictReader(fo)
    foout = open('data/national-quarterly.csv', 'w')
    writer = csv.writer(foout)
    writer.writerow(['Date', 'Composite-US'])
    for row in reader:
        year = row['YEAR'][:4]
        date = '%s-%02d-01' % (year, (int(row['QTR'][1])-1)*3+1)
        writer.writerow([date, row['COMPOSITE-US']])

process_national()
process_national_q()
