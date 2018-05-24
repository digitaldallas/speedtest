import pyspeedtest
import csv
from time import strftime

st = pyspeedtest.SpeedTest()

results={
        'datetime':strftime("%Y-%m-%d %H:%M:%S"),
        'ping': st.ping(),
        'download': st.download()/1000000,
        'upload': st.upload()/1000000
}

print(results)

with open('speedtest.results.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=results.keys())
    #writer.writeheader()
    writer.writerow(results)