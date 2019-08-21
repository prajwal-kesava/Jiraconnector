import pandas as pd
from projectkeys import project_not_archived_ids as pk_id
import os
import json
import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
from pandas.io.json import json_normalize
cp= ConfigParser()
cp.read( r"jiraprop.ini" )


JIRA_EMAIL = cp.get('user details','user')
JIRA_TOKEN =  cp.get('user details','apikey')
BASE_URL = cp.get('user details','URL')
API_URL = "/rest/agile/1.0/board?projectKeyOrId="
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


JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]

Emptydf=pd.DataFrame()
emp=pd.DataFrame()
for id in pk_id:
    API_URL_END=API_URL+id
    print(API_URL_END)
    respone_data=api_call(API_URL_END,HEADERS,BASIC_AUTH)
    data=json.loads(respone_data)
    work_data=json_normalize(data,record_path='values',errors='ignore',sep='_')
    work_data['project_id']=id
    Emptydf=Emptydf.append(work_data,ignore_index=True,sort=True)
    

# print(Emptydf.columns)    
Emptydf.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','name','type','project_id'],index=False)    
