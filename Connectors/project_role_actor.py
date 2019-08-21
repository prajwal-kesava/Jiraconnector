import pandas as pd
import json
import os
import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
from pandas.io.json import json_normalize
cp= ConfigParser()
cp.read( r"jiraprop.ini" )
JIRA_EMAIL = cp.get('user details','user')
JIRA_TOKEN = cp.get('user details','apikey')
BASE_URL = cp.get('user details','URL')
API_END_URL=cp.get('END URL','role')
API_URL = "/rest/api/3/"+API_END_URL
API_URL = BASE_URL+API_URL
print(API_URL)
BASIC_AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {'Content-Type' : 'application/json;charset=iso-8859-1'}
def api_call(url,header,authentication):
    response = requests.get(
    url,
    headers=header,
    auth=authentication
    )
    return response.text
response_data=api_call(API_URL,HEADERS,BASIC_AUTH)
d=json.loads(response_data)
print(d)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
print(JSON_FILE)
with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
	json.dump(d, f, ensure_ascii=False, indent=4)

# with open(JSON_FILE+".json") as f:
#     d=json.load(f)


    
work_data=json_normalize(data=d,sep="_")
work_data.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['self','name','id','description'],index=False)


