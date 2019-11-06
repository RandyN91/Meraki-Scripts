import requests
import time
import sys
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning #this is to ignore insecure HTTPS request to cloud (it doesnt recongize meraki dashboard)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('803e0aafb6c824c2d3ab49cd5512689140d5af1d')),
           'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'

counter = 0

def dbmCSQ(csq):#formula to convert CSQ Values to Signal %
    csq = csq[4:]
    csq = csq.split(",")
    rssi = (int(csq[0]) * 2) - 113
    percent = 2 * (rssi + 100)
    str(percent)
    return percent

print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)

networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers,
                        verify=False).json()

totalnetworks = len(networks)

print("Organization Info Retrieved")

with open('PercentCSVOutput.csv','w') as csvfile:
 filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
 filewriter.writerow(['Store','Cell Provider','Aircard','Status','Signal Strength'])
 csvfile.flush()

for networks in networks:

    sys.stdout.write("\r ---Pulling info from : " + networks['name'] + "     ("+str(counter)+"/"+str(totalnetworks)+")")
    time.sleep(0.25)
    sys.stdout.flush()
    counter = counter + 1

    if 'STR-' in networks['name']:



        devices = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()

        for devices in devices:

            if 'MX' in devices['model']:

                uplinks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks' + '/'
                                        + networks['id'] + '/' + 'devices' + '/' + devices['serial'] + '/' +
                                        'uplink', headers=headers, verify=False).json()

                for uplinks in uplinks:

                    try:
                        if 'Cellular' in uplinks['interface'] and 'Connecting' in uplinks['status'] and 'Unknown' in \
                                uplinks['provider']:
                            sys.stdout.write(" \n---Pulling info from : " + networks['name'] + " " +devices['model'] +
                            " " + devices['serial'])
                            print("\nThis Store's Aircard is in Connecting State, needs to be reseated")
                            sys.stdout.flush()

                    except KeyError:
                        print("-Invalid Cell Information received, Check Aircard")
                        print("\n")
                        break

                    except KeyError:
                        print("No Cell Data received from " + networks['name'])
                        print("\n")
                        break

                    try:
                        if 'Cellular' in uplinks['interface'] and 'Unknown' not in uplinks['signal']:

                            dbmvalue = dbmCSQ(str(uplinks['signal']))

                            if dbmvalue < 50: #Input Signal Threshold here
                                sys.stdout.write(" \n---Pulling info from : " + networks['name'] + " ")
                                print("\n")

                                filewriter.writerow([str(networks['name']),  str(uplinks['provider']), str(uplinks['model']), str(uplinks['status']), str(dbmvalue)+"%"])

                                print("Cellular Info : ")
                                print("--Signal Strength : " + str(dbmvalue) + "%" + " (RSSI is " + str(
                                    (dbmvalue / 2) - 100) + ")")
                                print("--Provider : " + uplinks['provider'])
                                print("--Model : " + uplinks['model'])
                                print("--Status : " + uplinks['status'])
                                sys.stdout.flush()
                                csvfile.flush()
                                print("\n")

                    except KeyError:
                         print("-Invalid Cell Information received, Check Aircard")
                    break

print("\nScript is Complete")

csvfile.close()














