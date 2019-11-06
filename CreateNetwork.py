import requests
import time
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('6bec40cf957de430a6f1f2baa056b99a4fac9ea0')),'Content-Type': 'application/json'}
OrgKey = '681155' # Meraki Sandbox

print("Start of Script")
print("\nGathering Organization Info from Sandbox Meraki Organization # : " + OrgKey)
networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers, verify=False).json()

payload = {'id': 'L_566327653141843049', 'organizationId': '681155', 'name': 'STR-1272', 'timeZone': 'America/New_York', 'tags': None, 'type': 'combined', 'disableMyMerakiCom': False, 'disableRemoteStatusPage': True}

#networks = requests.post(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers, verify=False,data=json.dumps(payload))

time.sleep(1)

print("Network Data Gathered")

for networks in networks:

    if 'combined' in networks['type']:

        devices = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()


        time.sleep(0.10)

        for devices in devices:

            if 'MX' in devices['model']:

                # print("\nNow getting Cell Information from " + devices['model'] +
                #      " " + devices['serial'])

                clients = requests.get(MERAKI_URL + 'devices' + '/' + devices['serial'] +
                                      '/' + 'clients?timespan=2592000', headers=headers, verify=False).json()
                try:

                 for clients in clients:
                    #print(clients)

                    if clients['vlan'] == 5:

                     policy = requests.get(MERAKI_URL + '/' + 'networks' + '/' + networks['id'] + '/' +
                               'clients/' + clients['mac'] + '/policy', headers=headers, verify=False).json()


                     for policy in policy:
                         print(policy)

                except KeyError as e:

                    badkey = e.args[0]
                    print("\nError in " + clients['ip'] + " at this Key : " + badkey + " for " + networks['name'] + "\n")

print("End of Script")