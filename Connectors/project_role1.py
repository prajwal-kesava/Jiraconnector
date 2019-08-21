import pandas as pd
import json
from projectkeys import project_not_archived_ids as pk_ids
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
# API_END_URL=cp.get('END URL','role')
# API_URL = "/rest/api/3/"+API_END_URL
API_URL = "https://tapestrykpi.atlassian.net/rest/api/3/role"
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
# print(d)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
print(JSON_FILE)
# with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
# 	json.dump(d, f, ensure_ascii=False, indent=4)

# with open(JSON_FILE+".json") as f:
#     d=json.load(f)
roles_id=[]

for role in d:
    roles_id.append(role['id'])



# print(roles_id) 
# print(project_id)  
df=pd.DataFrame()
for i in pk_ids:
    for j in roles_id:
        # w=pd.DataFrame({'project_id':[i],'role_id':[j]})
        API_URL_END_2="https://tapestrykpi.atlassian.net/rest/api/3/project/"+f"{i}"+"/role/"+f"{j}"
        print(API_URL_END_2)
        response=api_call(API_URL_END_2,HEADERS,BASIC_AUTH)
        data=json.loads(response)
        work_data=json_normalize(data,errors='ignore',sep='_')
        work_data['project_id']=i
        work_data['role_id']=j
        # role_prj=pd.concat([w,work_data],axis=1)
        df=df.append(work_data,ignore_index=True,sort=True)
#drop row if there is empty fields
df=df.dropna()    
df.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['project_id','role_id','name'],index=False)


