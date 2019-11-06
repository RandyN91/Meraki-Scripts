import requests
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'
startTime = time.time()

print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)
networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers, verify=False).json()
print("Organization Info Retrieved")

for networks in networks: #cycle through JSON Data
    #search for key which matches store value
    #print(networks)

    sys.stdout.write("\r ---Pulling info from : " + networks['name'])
    time.sleep(0.25)
    sys.stdout.flush()

    if 'STR-' in networks['name']:

        #print("\nGathering Device Data from : " + networks['name'])
        devices = requests.get(MERAKI_URL + 'organizations'+'/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()
        #print(devices)
        for devices in devices:

            if 'MS' in devices['model']:
                print("\n Now getting Information from " + devices['model'] +
                  " " + devices['serial'])

                clients = requests.get(MERAKI_URL + 'devices' + '/' + devices['serial'] +
                                       '/' + 'clients?timespan=2592000', headers=headers, verify=False).json()
                #print(clients)
                try:
                    for clients in clients:
                        #print(clients)
                        if '.15' in str(clients['ip']):
                         print("Network Name : "+networks['name'])
                         print("Device MAC : "+clients['mac'])
                         print("Device Desc : "+str(clients['description']))
                         print("Device mdnsName : " + str(clients['mdnsName']))
                         print("Device dhcpHostname : " + str(clients['dhcpHostname']))
                         print("Device VLAN : " +str(clients['vlan']))
                         print("Device IP : " +str(clients['ip'] + "\n"))

                except KeyError as e:

                    badkey = e.args[0]

                    print("\n Error at this JSON Key : " + badkey + " for " + networks['name'] + "\n")

print ('\nThe script took {0} seconds !'.format(int(time.time() - startTime)))




'''
 and str(clients['mac']).startswith('f0:92:1c' or '94:57:a5' or '30:e1:71' or '2c:44:fd' \
                           'f4:30:b9' or '5c:52:82' or 'a0:d3:c1'or '9c:b6:54' or '3c:52:82' \
                        or '58:20:b1' or 'a0:d3:c1' or 'fc:15:b4' or 'f0:92:1c' or '14:58:d0' \
                        or 'd0:bf:9c' or 'a4:5d:36' or '9c:b6:54' or '6c:c2:17' or 'd4:c9:ef' \
                        or 'c4:34:6b' or '40:b0:34' or 'fc:3f:db' or 'f4:30:b9' or 'a0:8c:fd' \
                        or 'dc:4a:3e' or 'ec:8e:b5' or '9c:b6:54')
                        
                        'dell' or 'Dell' in clients['description'] or \
                            'dell' or 'Dell' in clients['mdnsName'] or \
                            'dell' or 'Dell' in clients['dhcpHostname'] \
                            or
'''