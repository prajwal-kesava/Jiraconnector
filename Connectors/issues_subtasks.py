import pandas as pd 
from projectKeys import project_not_archived_ids as pid
import os
import json
import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
from pandas.io.json import json_normalize
cp= ConfigParser()
cp.read( r"jiraprop.ini" )
JIRA_EMAIL = cp.get('user details','user')
JIRA_TOKEN = cp.get('user details','apikey')
BASE_URL = cp.get('user details','server')
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]

# API_END_URL=cp.get('END URL','issues')
API_URL = "/rest/api/3/search"
API_URL = BASE_URL+API_URL+"?jql=project="
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
df=pd.DataFrame()
total=int(0)
for prj in pid:
    API_URL_END=API_URL+str(prj)+"&maxResults=1000"
    print(API_URL_END)
    response_data=api_call(API_URL_END,HEADERS,BASIC_AUTH)
    data=json.loads(response_data)
    # total=total+int(data['total'])
    work_data=json_normalize(data,record_path=['issues',['fields','subtasks']],errors='ignore',sep='_')
    df=df.append(work_data,ignore_index=True,sort=True)
df.to_csv(JSON_FILE+".csv",index=False)

print(total)

