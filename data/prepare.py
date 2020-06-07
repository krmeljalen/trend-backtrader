import sys
import csv
import json
from datetime import datetime

#%Y-%m-%d %H:%M:%S

with open('btc_hints2.csv', 'w') as result:
    with open('btc_hints.json') as json_file:
        writer = csv.writer(result, lineterminator='\n')
        for row in json_file:
            data = json.loads(row)
            if "btcusd" in data:
                new_line = []
                d = datetime.fromtimestamp(float(data["timestamp"]))
                new_line.append(d.strftime("%Y-%m-%d %H:%M:%S"))
                new_line.append(data["btcusd"]["down_confidence"].replace('%',''))
                new_line.append(data["btcusd"]["up_confidence"].replace('%',''))
                writer.writerow(new_line)

result.close()
