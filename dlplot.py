import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from statistics import mean
import time

while True:
    # Load CSV
    data = pd.read_csv('data//st_results.csv')

    tslist = data['Timestamp'].tolist()
    dllist = data['Download in Mbps'].tolist()

    tlen = len(tslist)
    dlen = len(dllist)

    # Only graph the last 200 (about 3 days worth)
    records = 200
    if tlen > records:
        n = tlen - records
        tslist =tslist[n:]
        dllist = dllist[n:]
        avg = mean(dllist)  # Get the average


    plt.title(f"Average Download: {avg}")
    plt.xlabel('Timestamp')
    plt.xticks(rotation=90)
    plt.ylabel('Download')

    plt.plot(tslist, dllist)  # Plot the Download Chart

    plt.subplots_adjust(left=0.057, bottom=0.248, right=0.976, top=0.97, wspace=0.2, hspace=0.2)   # Customize the chart size
    plt.show()  # display 

    print("Waiting 1 hour to refresh...")
    time.sleep(3600) # 3600 is 1 hour
    plt.close()