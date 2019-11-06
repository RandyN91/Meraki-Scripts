import requests
import time
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'

print("Start of Script")
print("\nGathering Organization Info from Organization # : " + OrgKey)
orgs = requests.get(MERAKI_URL + 'organizations'+'/' + OrgKey + '/' + 'networks', headers=headers, verify=False).json()
print("Organization Info Loaded")
totalorgs = len(orgs)
counter = 0
for orgs in orgs: #cycle through JSON Data
    #search for key which matches store value
    sys.stdout.write("\r ---Pulling info from : " + orgs['name'] + "     ("+str(counter)+"/"+str(totalorgs)+")")
    time.sleep(0.25)
    sys.stdout.flush()
    counter = counter + 1
    if 'STR-' in orgs['name']:
        #print("\nGathering Device Data from : " + orgs['name'])
        devices = requests.get(MERAKI_URL + 'organizations'+'/' + OrgKey +
                               '/' + 'networks' + '/' + orgs['id'] + '/' +
                               'devices', headers=headers, verify=False).json()

        for devices in devices:
            if 'MS' in devices['model']:
                #print("Now getting Information from " + devices['model'] +
                     # " " + devices['serial'])
                clients = requests.get(MERAKI_URL + 'devices' + '/' + devices['serial']+
                                       '/' + 'clients?timespan=2592000',headers=headers, verify=False).json()
                #print(clients)
                for clients in clients:
                    if '23' in clients['switchport']:
                        print("\nIn " + orgs['name'] + " on " + devices['model'])
                        print("****Switchport " + clients['switchport'] + " is in use by : " + str(clients['mac']) + " " + str(clients['ip']))
                    elif '24' in clients['switchport']:
                        print("\nIn " + orgs['name'] + " on " + devices['model'])
                        print("****Switchport " + clients['switchport'] + " is in use by : " + str(clients['mac']) + " " + str(clients['ip']))

time.sleep(0.20)