import requests
import sys
import time
import csv
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),
           'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'
startTime = time.time()
counter =0
print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)

networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers,
                        verify=False).json()

totalnetworks = len(networks)

print("Organization Info Retrieved")



with open('IpadCSVOutput.csv', 'w') as csvfile:
 filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

 filewriter.writerow(['Store', 'Device MAC', 'Device Desc', 'Device VLAN', 'Device mdnsName', 'Device IP'])
 csvfile.flush()

 for networks in networks:

    sys.stdout.write("\r ---Pulling info from : " + networks['name'] + "     ("+str(counter)+"/"+str(totalnetworks)+")")
    time.sleep(0.10)
    sys.stdout.flush()
    counter = counter + 1

    if 'STR-' in networks['name']:

        # print("\nGathering Device Data from : " + networks['name'])
        devices = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()
        # print(devices)
        for devices in devices:

            if 'MS' in devices['model']:
                print("\n Now getting Information from " + devices['model'] +
                      " " + devices['serial'])

                clients = requests.get(MERAKI_URL + 'devices' + '/' + devices['serial'] +'/' + 'clients?timespan=2592000', headers=headers, verify=False)

                try:

                    clients = json.loads(clients.content.decode('utf-8'))

                except json.JSONDecodeError as e:
                    print("Error in JSON client Data from " + networks['name'])

                try:
                    for clients in clients:

                        if '41' in str(clients['vlan']):

                           print(clients)
                           filewriter.writerow([str(networks['name']), str(clients['mac']), str(clients['description']),str(clients['vlan']), str(clients['mdnsName']),str(clients['ip'])])
                           csvfile.flush()

                except Exception as e:

                   badkey = e.args[0]

                   print("\n Error in this Network Data : " + badkey + " for " + networks['name'] + "\n")

print('\nThe script took {0} seconds !'.format(int(time.time() - startTime)))

csvfile.close()
