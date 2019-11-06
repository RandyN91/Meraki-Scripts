import requests
import time
import sys
#import smtplib


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

##Meraki Constants
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
headers = {'x-cisco-meraki-api-key': format(str('KEY OBSCURED')),'Content-Type': 'application/json'}
OrgKey = 'KEY OBSCURED'
startTime = time.time()
#mailserver = smtplib.SMTP('smtp.jcrew.com',25)
#mailserver.login()
print("Start of Script")
print("\nGathering Organization Info from J.CREW Meraki Organization # : " + OrgKey)
networks = requests.get(MERAKI_URL + 'organizations' + '/' + OrgKey + '/' + 'networks', headers=headers, verify=False).json()
totalnetworks = len(networks)
print("\nOrganization Info Retrieved " + "from " + str(totalnetworks) + " Networks")

i=0


for networks in networks:
 try:
    NoData = []

    if 'DSR' in str(networks['tags']) and 'L_651896046061885123' in str(networks['configTemplateId']):

        sys.stdout.write("\r ---Pulling info from : " + networks['name']+'\n')
        time.sleep(0.25)
        sys.stdout.flush()

        devices = requests.get(MERAKI_URL + 'organizations' +'/' + OrgKey +
                               '/' + 'networks' + '/' + networks['id'] + '/' +
                               'devices', headers=headers, verify=False).json()
        if devices == NoData:
            print("\n\nStore " + networks['name'] + " has no Data returned, It does not have devices bound to it. Check Dashboard.\n")

        for devices in devices:

            if 'MX' in devices['model']:

                uplinks = requests.get(MERAKI_URL + 'organizations' +'/' + OrgKey + '/' + 'networks' + '/'
                                       + networks['id'] + '/' + 'devices' + '/' + devices['serial'] + '/' +
                                   'uplink', headers=headers, verify=False).json()

                for uplinks in uplinks:

                    try:

                        if 'WAN 1' in uplinks['interface']:
                            print(uplinks)
                            #print("\nGathering Device Data from : " + networks['name'])
                            #print("Uplink " + uplinks['interface'] + " is in failed state")
                            #print("It had this IP : " + str(uplinks['ip']))
                            #print("It had this Gateway : " + str(uplinks['ip']))
                            #print("Was it Static?  : " + str(uplinks['usingStaticIp'])+"\n")
                    except KeyError as e:
                        badkey = e.args[0]
                        print("\nError in " + uplinks['interface'] + " at this Key : " + badkey + " for " + networks['name'] + "\n")
 except KeyError:
     pass
print ('\nThe script took {0} seconds !'.format(int(time.time() - startTime)))