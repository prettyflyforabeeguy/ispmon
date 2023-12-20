import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from statistics import mean
import time

while True:
    # Load CSV
    data = pd.read_csv('data//st_results.csv')

    tslist = data['Timestamp'].tolist()
    ullist = data['Upload in Mbps'].tolist()

    tlen = len(tslist)
    ulen = len(ullist)

    # Only graph the last 200 (about 3 days worth)
    records = 200
    if tlen > records:
        n = tlen - records
        tslist =tslist[n:]
        ullist = ullist[n:]
        avg = mean(ullist)  # Get the average

    plt.title(f"Average Upload: {avg}")
    plt.xlabel('Timestamp')
    plt.xticks(rotation=90)
    plt.ylabel('Upload') 

    plt.plot(tslist, ullist)  # Plot the Upload Chart

    plt.subplots_adjust(left=0.057, bottom=0.248, right=0.976, top=0.97, wspace=0.2, hspace=0.2)
    plt.show()  # display 

    print("Waiting 1 hour to refresh...")
    time.sleep(3600) # 3600 is 1 hour
    plt.close()