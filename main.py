import uuid
import requests
import json
import os

client_id = str(uuid.uuid4())
current_path = os.getcwd()

office_response = requests.get("https://endpoints.office.com/endpoints/worldwide?clientrequestid={}".format(client_id))
office_list = office_response.json()

sorted_office_list = {}

for item in office_list:
    if item.get('ips') != None:
        ip_list = item['ips']
    else:
        ip_list = False
    if item['serviceAreaDisplayName'] not in sorted_office_list and ip_list:
        sorted_office_list[item['serviceAreaDisplayName']] = ip_list
    elif ip_list:
        sorted_office_list[item['serviceAreaDisplayName']].extend(ip_list)

for key in sorted_office_list.keys():
    with open(f"{current_path}/artifacts/{key}.txt", 'w') as out_file:
        for item in sorted_office_list[key]:
            out_file.write("%s\n" % item)

