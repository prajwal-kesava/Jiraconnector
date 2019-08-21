import pandas as pd
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
BASE_URL = cp.get('user details','URL')
API_END_URL=cp.get('END URL','projects')
API_URL = "/rest/api/3/"+API_END_URL
API_URL = BASE_URL+API_URL
# print(API_URL)
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
project_response_data=json.loads(response_data)
# print(project_response_data)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
# with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
# 	json.dump(project_response_data, f, ensure_ascii=False, indent=4)

project_not_archived_ids=[]
projectCategory_id=[]
for project in project_response_data:
    for key in project.keys():
        if(key=='projectCategory'):
            if(project[key]['name'] != 'Archived'):
                        project_not_archived_ids.append(project['id'])
                        projectCategory_id.append(project[key]['id'])
# rest/api/3/projectCategory/{id}'
print(projectCategory_id)
distinct_id = set()
uniq = [x for x in projectCategory_id if x not in distinct_id and not distinct_id.add(x)]
print(distinct_id)

df=pd.DataFrame()
for id in distinct_id:
    API_URL=BASE_URL+"/rest/api/3/projectCategory/"+id
    print(API_URL)
    response=api_call(API_URL,HEADERS,BASIC_AUTH)
    data=json.loads(response)
    work_data=json_normalize(data,errors='ignore',sep='_')
    df=df.append(work_data,sort=True,ignore_index=True)
df.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','name','description'],index=False)

