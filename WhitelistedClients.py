import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'

print("Start of Script")
print("\nGathering Organization Info from Organization # : " + OrgKey)
networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers, verify=False).json()
print("Organization Info Loaded")

for networks in networks:

    if 'STR-2' in networks['name']:

        print("\nGathering Device Data from : " + networks['name'])
        devices = requests.get(MERAKI_URL + 'organizations' +'/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()

        for devices in devices:

            if 'MX' in devices['model']:
                print("Now getting Information from " + devices['model'] +
                      " " + devices['serial'])
                clients = requests.get(MERAKI_URL + 'devices' + '/' + devices['serial']+
                                       '/' + 'clients?timespan=2592000',headers=headers, verify=False).json()
                print("\nThe Following Clients are Whitelisted at " + networks['name'])
                for clients in clients:

                        if clients['vlan'] == int(41):

                            policy = requests.get(MERAKI_URL +'/' + 'networks' + '/' + networks['id'] + '/' +
                               'clients' + '/' + clients['mac'] + '/' + 'policy?timespan=2592000', headers=headers, verify=False).json()
                            try:

                                if 'Whitelisted' in policy['type']:

                                    print("\n-Device Description : " + clients['description'])
                                    print("-Device MAC Address : " + clients['mac'])
                                    print("-Device VLAN ID  : " + str(clients['vlan']))
                                    print("-Device IP Address  : " + str(clients['ip']))

                            except:
                                KeyError
