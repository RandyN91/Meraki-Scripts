import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'

def dbmCSQ(csq):
    csqisolate = csq.split(",")[0]
    formattedcsq = int(csqisolate[4:])
    rssi = int(formattedcsq) * int(2) - 113
    percent = 2 * (rssi+100)
    str(percent)
    return percent

print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)
networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers, verify=False).json()
print("Organization Info Retrieved")


for networks in networks:
    NoData = []

    if 'STR-' in networks['name']:

        #print("\nGathering Device Data from : " + networks['name'])
        devices = requests.get(MERAKI_URL + 'organizations' +'/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()
        if devices == NoData:
            print("Store " + networks['name'] + " has no Data returned, It does not have devices bound to it. Check Dashboard.")

        for devices in devices:

            if 'MX' in devices['model']:

                #print("\nNow getting Cell Information from " + devices['model'] +
                 #     " " + devices['serial'] + " at " + networks['name'])

                uplinks = requests.get(MERAKI_URL + 'organizations' +'/' + OrgKey + '/' + 'networks' + '/'
                                       + networks['id'] + '/' + 'devices' + '/' + devices['serial'] + '/' +
                                   'uplink', headers=headers, verify=False).json()
                #print(uplinks)
                if uplinks is None:
                    print("This store is not returning data, check if it is live in dashboard " + networks['name'])


                for uplinks in uplinks:
                    #print(uplinks)
                    if 'Cellular' in uplinks['interface'] and 'Connecting' in uplinks['status'] and 'Unknown' in uplinks['provider']:
                        try:
                            print("This Store's Aircard is in Connecting State, needs to be reseated " + networks['name'])
                            break
                        except KeyError:
                            print("No Cell Data received from " + networks['name'])
                            break


                    elif 'Cellular' not in uplinks['interface']:

                        #print("This Store's Aircard does NOT have an aircard, it has the following WAN Connection : ")
                        try:
                            while 'WAN' in uplinks['interface']:
                                #print("-"+uplinks['interface'])
                                #print("-"+uplinks['ip'])
                                #print("-"+uplinks['status'])
                                break

                        except KeyError:
                                print("-No WAN Data Received from " + networks['name'] + " Check Interfaces or if Store is Up.")
                                break

                    '''elif 'Cellular' in uplinks['interface'] and 'Unknown' not in uplinks['signal']:
                        try:
                                dbmvalue = dbmCSQ(uplinks['signal'])
                                print("Cellular Info : ")
                                print("--Signal Strength : " + str(dbmvalue) +"%"+" (RSSI is " + str((dbmvalue/2)-100)+")")
                                print("--Provider : " + uplinks['provider'])
                                print("--Model : " + uplinks['model'])
                                print("--Status : " + uplinks['status'])
                                break
                        except KeyError:
                                print("-Invalid Cell Information received, Check Aircard")
                                break
                    elif 'Cellular' in uplinks['interface'] and 'Unknown' not in uplinks['signal']:
                        try:
                                dbmvalue = dbmCSQ(uplinks['signal'])
                                print("Cellular Info : ")
                                print("--Signal Strength : " + str(dbmvalue) +"%"+" (RSSI is " + str((dbmvalue/2)-100)+")")
                                print("--Provider : " + uplinks['provider'])
                                print("--Model : " + uplinks['model'])
                                print("--Status : " + uplinks['status'])
                                break
                        except KeyError:
                                print("-Invalid Cell Information received, Check Aircard")
                                break
'''

time.sleep(0.10)















