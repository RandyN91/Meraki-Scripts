import requests
import time
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),
           'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'


def dbmCSQ(csq):
    csq = csq[4:]
    csq = csq.split(",")
    rssi = (int(csq[0]) * 2) - 113
    percent = 2 * (rssi + 100)
    str(percent)
    return percent


'''
CSQ is failing at site 262 becaue the first value of the csq string is 1 digit , redo the function to split that value and remove the first number only 
'''

print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)
networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers,
                        verify=False).json()
print("Organization Info Retrieved")


for networks in networks:

    if 'STR-' in networks['name']:

        time.sleep(0.10)

        devices = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()

        for devices in devices:

            if 'MX' in devices['model']:

                # print("\nNow getting Cell Information from " + devices['model'] +
                #      " " + devices['serial'])

                uplinks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks' + '/'
                                       + networks['id'] + '/' + 'devices' + '/' + devices['serial'] + '/' +
                                       'uplink', headers=headers, verify=False).json()

                for uplinks in uplinks:

                    try:
                        if 'Cellular' in uplinks['interface'] and 'Connecting' in uplinks['status'] and 'Unknown' in \
                                uplinks['provider']:
                            sys.stdout.write(" \n---Pulling info from : " + networks['name'] + " ")
                            print("\nThis Store's Aircard is in Connecting State, needs to be reseated")
                            sys.stdout.flush()

                    except KeyError:
                        print("-Invalid Cell Information received, Check Aircard")


                    except KeyError:
                        print("No Cell Data received from " + networks['name'])
                        break

                    try:
                        if 'Cellular' in uplinks['interface'] and 'Unknown' not in uplinks['signal']:

                            # print(uplinks['signal'])
                            dbmvalue = dbmCSQ(str(uplinks['signal']))
                            if dbmvalue < 50:
                                sys.stdout.write(" \n---Pulling info from : " + networks['name'] + " ")
                                print("\n")
                                print("Cellular Info : ")
                                print("--Signal Strength : " + str(dbmvalue) + "%" + " (RSSI is " + str(
                                    (dbmvalue / 2) - 100) + ")")
                                print("--Provider : " + uplinks['provider'])
                                print("--Model : " + uplinks['model'])
                                print("--Status : " + uplinks['status'])
                                sys.stdout.flush()

                    except KeyError:
                        print("-Invalid Cell Information received, Check Aircard")
                        break
time.sleep(0.25)















