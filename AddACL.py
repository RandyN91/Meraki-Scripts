import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = '605271'

print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)
ACL = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' +  '/vpnFirewallRules', headers=headers, verify=False).json()
print("Organization Info Retrieved")
for ACL in ACL:

    print(ACL)
