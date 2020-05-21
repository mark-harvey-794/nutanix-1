import requests
import urllib.request
import pandas as pd
import ipaddress
import urllib3
from requests.auth import HTTPBasicAuth
import json

def GetCluster():
    print("What's Prism VIP address? ")
    VIP = input()
    if ipaddress.ip_address(VIP):
           print ("You typed right ip format")
    else:
      print ("You typed wrong ip format")
      print ("Existing")
    print("What is the Prism UI User which has admin role? ")
    username = input()
    print("What is the password for the Prism UI User? ")
    password = input()
    return(VIP,username,password)

def PrismMenu(VIP):
    #baseUrl=str()
    baseUrl = "https://"+VIP+":9440/PrismGateway/services/rest/v2.0/"
    print("What kind of information do you want to collect?")
    print("########## MENU ########## ")
    print("Type 1: cluster info")
    print("Type 2: disk info")
    seLection = input()
    return seLection

def PrismDiskInfo(VIP,username,password):
    baseUrl = "https://"+VIP+":9440/PrismGateway/services/rest/v2.0/"
    print("########## Listing Disks.... ########## in %s" %baseUrl)
    subpath = '/disks'
    ResPonse = requests.get(baseUrl+subpath, headers={'Accept': 'application/json'}, verify=False, auth=HTTPBasicAuth(username, password))
    ResPonse_json = json.loads(ResPonse.text)
    disk_count=len(ResPonse_json['entities'])
    print("########## The number of disks is ########## %s" %disk_count)
    diskinfo={}
    for i in range(disk_count):
        mount_path = ResPonse_json['entities'][i]['disk_hardware_config']['mount_path']
        disk_sn = ResPonse_json['entities'][i]['disk_hardware_config']['serial_number']
        print ("%s || disk mountpath & serial number: " %i)
        print(mount_path)
        print(disk_sn)
        print("........")

def PrismClusterInfo(VIP,username,password):
    baseUrl = "https://"+VIP+":9440/PrismGateway/services/rest/v2.0/"
    print("########## Show Cluster config detail.... in %s" %baseUrl)
    subpath = '/cluster'
    Cluster_detail = requests.get(baseUrl+subpath, headers={'Accept': 'application/json'}, verify=False, auth=HTTPBasicAuth(username, password))
    Cluster_detail_dict = json.loads(Cluster_detail.text)
    #Cluster detail is saved as dictionary, printing key and value 
    for k,v in Cluster_detail_dict.items():
        print(k,":",v)
        print("#############")

if __name__ == '__main__':
    cluster = GetCluster()
    VIP = cluster[0]
    username = cluster[1]
    password = cluster[2]
    select = PrismMenu(VIP)
    if select == str(1):
        PrismClusterInfo(VIP,username,password)
    elif select == str(2):
        PrismDiskInfo(VIP,username,password)
    else :
        print("Selected wrong option...")
        exit()