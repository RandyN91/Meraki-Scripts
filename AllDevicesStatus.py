import requests
import time
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'
startTime = time.time()
print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)
devices = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'deviceStatuses', headers=headers, verify=False).json()
totalnetworks = len(devices)
print("\nOrganization Info Retrieved " + "from " + str(totalnetworks) + " Devices")

for devices in devices:
  try:
   if 'offline' in devices['status']:
    print(devices)
  except KeyError as e:

      badkey = e.args[0]
      print("\nError in " + devices['name'] + " at this Key : " + badkey + "\n")
