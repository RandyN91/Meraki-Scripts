import requests
import time
import sys
import csv

from requests.packages.urllib3.exceptions import InsecureRequestWarning #this is to ignore insecure HTTPS request to cloud (it doesnt recongize meraki dashboard)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),
           'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'

counter = 0

print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)

networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers,
                        verify=False).json()

totalnetworks = len(networks)

print("Organization Info Retrieved")

with open('PatrickCSVOutput.csv','w') as csvfile:
 filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
 filewriter.writerow(['Network Name', 'Device Desc', 'Device VLAN', 'Device MAC', 'Device IP'])
 csvfile.flush()

 for networks in networks:
    counter = counter + 1
    sys.stdout.write("\r ---Pulling info from : " + networks['name'] + "     ("+str(counter)+"/"+str(totalnetworks)+")")
    time.sleep(0.25)
    sys.stdout.flush()

    if 'STR-' in networks['name']:

        devices = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()

        for devices in devices:

                if 'MS' in devices['model']:
                    print("\n Now getting Information from " + devices['model'] +
                          " " + devices['serial'])

                    clients = requests.get(MERAKI_URL + 'devices' + '/' + devices['serial'] +
                                           '/' + 'clients?timespan=192000', headers=headers, verify=False).json()
                    # print(clients)
                    try:

                        for clients in clients:
                            # print(clients)
                            if '.15' in str(clients['ip']):
                                filewriter.writerow(
                                    [str(networks['name']), str(clients['description']), str(clients['vlan']),
                                     str(clients['mac']), str(clients['ip'])])

                                print("Network Name : " + networks['name'])
                                print("Device MAC : " + clients['mac'])
                                print("Device Desc : " + str(clients['description']))
                                print("Device mdnsName : " + str(clients['mdnsName']))
                                print("Device dhcpHostname : " + str(clients['dhcpHostname']))
                                print("Device VLAN : " + str(clients['vlan']))
                                print("Device IP : " + str(clients['ip'] + "\n"))


                    except KeyError:
                         print("-Invalid Client Information received, Check Network " + networks['name'])
                    break

print("\nScript is Complete")

csvfile.close()














