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
 if '10.101.' in ACL['srcCidr'] or '10.101.' in ACL['destCidr']:
    #print(ACL['comment'])
    print("ACL Comment : " + ACL['comment'] + '\n' + "Source IP   : "  + ACL['srcCidr']+ '\n' + "Dest IP     : " + ACL['destCidr']+ '\n' +"Protocol    : " + ACL['protocol']+ '\n' + "SrcPort     : " + ACL['srcPort']+ '\n' + "DstPort     : " +ACL['destPort'])
    print("---------------------------------------------------------------------------")

'''
for networks in networks:
    if 'STR-1023' in networks['name']:
        mxFW = requests.get(MERAKI_URL + '/networks/' + networks['id'] + '/vpnFirewallRules', headers=headers, verify=False).json()
        for mxFW in mxFW:
            print(mxFW['policy'] + ' '+ mxFW['protocol']+ ' '+ mxFW['destCidr']+' '+  mxFW['destPort']+ '     ' + mxFW['comment'])
'''