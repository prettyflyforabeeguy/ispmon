# PrettyFlyForABeeGuy 11/4/2023. 
# Regularly test your ISPs speed and log the results.
# Using the aarch64 Speedtest by Ookla utility: https://www.speedtest.net/apps/cli
# To easily view the .csv file from the command line:
# cat data/st_results.csv | perl -pe 's/((?<=,)|(?<=^)),/ ,/g;' | column -t -s, | less -S 

import time, datetime
import logging
import os
import sys
import csv
import re

class ISPMonitor:
    def __init__(self):
        logging.basicConfig(filename='debug.log', format='%(asctime)s - %(message)s', level=logging.INFO)
        self.cmd = "./speedtest"
        self.csvcolumnheaders = ["Timestamp", "Server", "ISP", "Idle Latency", "Download", "Upload", "Packet Loss", "Result URL" ]

    def log_output(self,fname, data, method):
        logging.info("Writing to text file for speed test results.")
        #Store API results in a file
        filepath = "data/" + fname
        if os.path.isfile(filepath):
            pass
        try:
            file = open(filepath, method)
            file.close()
            fd = os.open(filepath, os.O_RDWR)
            line = str.encode(data)
            numBytes = os.write(fd, line)
            #print(f"Creating {filepath} bytes:{numBytes}")
            os.close(fd)

        except:
            print("Failed to write to /data")
            logging.exception("Exception occurred: Failed to write to /data in log_output function.")

    def readText(self):
        logging.info("Reading the text file for speed test results.")
        #print("Reading speed test results...")
        mylines = []
        with open ('data/speedtest.txt', 'rt') as myfile:
            for myline in myfile:
                myline = myline.strip('\n')
                myline = myline.strip('\t')
                mylines.append(myline.strip())
        mylines.remove("")
        mylines.remove('')
        #print(mylines)

        return mylines

    def clean_string(self,s):
        pattern = r',| '
        return re.sub(pattern, ' ', s)

    def resultCleanup(self, rlist):
        logging.info("Cleaning up results.")
        #print("Preparing .csv payload...")
        server = rlist[1]
        isp = rlist[2]
        latency = rlist[3]
        download = rlist[5]
        dlatency = rlist[6]
        upload = rlist[8]
        ulatency = rlist[9]
        ploss = rlist[10]
        rurl = rlist[11]

        server = server.split("Server:",1)[1]
        isp = isp.split("ISP:",1)[1]
        latency = latency.split("Idle Latency:",1)[1]
        download = download.split("Download:",1)[1]
        upload = upload.split("Upload:",1)[1]
        ploss = ploss.split("Packet Loss:",1)[1]
        rurl = rurl.split("Result URL:",1)[1]

        server = self.clean_string(server)
        server = server.strip(" ")
        isp = self.clean_string(isp)
        isp = isp.strip(" ")
        latency = self.clean_string(latency)
        latency = latency.strip(" ")
        download = self.clean_string(download)
        download = download.strip(" ")
        dlatency = self.clean_string(dlatency)
        dlatency = dlatency.strip(" ")
        download = download + " " + dlatency
        upload = self.clean_string(upload)
        upload = upload.strip(" ")
        ulatency = self.clean_string(ulatency)
        ulatency = ulatency.strip(" ")
        upload = upload + " " + ulatency
        ploss = self.clean_string(ploss)
        ploss = ploss.strip(" ")
        rurl = self.clean_string(rurl)
        rurl = rurl.strip(" ")
        payload = [server,isp, latency, download, upload, ploss, rurl]

        return payload


    def createCSV(self, csvfile):
        logging.info("Creating the .csv file if it doesn't exist.")
        if os.path.isfile(csvfile):
            pass
        else:
            try:
                with open(csvfile, 'w', newline='') as file:
                    fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    fwriter.writerow(self.csvcolumnheaders)
            except IOError:
                print(f"Error: Unable to create {csvfile}")
                logging.exception("Exception occurred: Failed to create .csv file in createCSV function.")


    def writeCSV(self, csvfile, payload):
        logging.info("Writing data to the .csv file.")
        try:
            print("Writing to .csv file...")
            with open(csvfile, 'a', newline='') as file:
                fwriter = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                fwriter.writerow(payload)
        except IOError:
            print(f"Error: Unable to write to {csvfile}")
            logging.exception("Exception occurred: Failed to write to .csv file in writeCSV function.")


    def speedTest(self):
        logging.info("executing ./speedtest")
        try:
            command = f"{self.cmd}"
            st = os.popen(command)
            st_list = st.read()
            print(st_list)
            self.log_output("speedtest.txt", st_list, 'w+')
        except Exception as e:
            print(f"Failed to perform speedtest. {e}")
            logging.exception("Exception occurred: Failed to complete speedTest. %s", e)


    def main(self):
        waittime = 30 # Specify how many minutes to wait between speed tests.
        waittime = int(waittime) * 60
        while True:
            print("Getting speedtest.net results.  This will take a few minutes...")
            timestamp = datetime.datetime.now()
            print(timestamp)
            _ispm.speedTest()
            rlist = _ispm.readText()
            payload =_ispm.resultCleanup(rlist)
            payload.insert(0, timestamp)
            _ispm.createCSV("data/st_results.csv")
            _ispm.writeCSV("data/st_results.csv", payload)

            print(datetime.datetime.now())
            print(f"Waiting {(waittime / 60)} minute(s) before checking again.")
            time.sleep(int(waittime))

if __name__ == '__main__':
    logging.info("Start program.")
    _ispm = ISPMonitor()
    welcome = f"""***********************************************************************************
*   Welcome to the ISP Monitoring tool.  This python tool is a wrapper for        *
*   the Speedtest by Ookla utility: https://www.speedtest.net/apps/cli            *
*   ISPMON allows you to check your ISPs speeds at a designated interval and      *
*   log the results in a .csv file.                                               *
***********************************************************************************"""
    print(welcome)
    _ispm.main()
