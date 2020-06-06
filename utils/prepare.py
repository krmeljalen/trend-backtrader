import csv
from datetime import datetime

#%Y-%m-%d %H:%M:%S
with open('bitstampUSD_1-min_data_2012-01-01_to_2020-04-22.csv', 'r') as source:
    with open('bitcoin.csv', 'w') as result:
        writer = csv.writer(result, lineterminator='\n')
        reader = csv.reader(source)
        source.readline()
        for row in reader:
            ts = row[0]
            d = datetime.fromtimestamp(float(ts))
            row[0] = d.strftime("%Y-%m-%d %H:%M:%S")
            if ts != "":
                writer.writerow(row)
source.close()
result.close()
