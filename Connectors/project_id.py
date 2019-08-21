import pandas as pd
import projectkeys as pk
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
API_END_URL=cp.get('END URL','projects')
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
# response_data=api_call(API_URL,HEADERS,BASIC_AUTH)
# project_response_data=json.loads(response_data)
# print(project_response_data)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]

df=pd.DataFrame()
# /rest/api/3/project/{projectIdOrKey}
for projectKeyOrId in pk.project_not_archived_ids:
    API_PROJECT_ID_URL=API_URL+"/"+projectKeyOrId
    print(API_PROJECT_ID_URL)
    response=api_call(API_PROJECT_ID_URL,HEADERS,BASIC_AUTH)
    projectId_data=json.loads(response)
    work_data=json_normalize(projectId_data,errors='ignore',sep="_")
    df=df.append(work_data,ignore_index=True,sort=True)
df.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','key','description','lead_active','lead_displayName','name','projectCategory_description','projectCategory_id' ,'projectCategory_name'],index=False) 

# with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
# 	json.dump(projectId_data, f, ensure_ascii=False, indent=4)

   

# with open(JSON_FILE+".json") as f:
#     d=json.load(f)

# meta_data=[]
# record_data=''

# # print(type(d))
# if(type(d)==list):
#     for li in d:
#         for key,value in li.items():
#             if(isinstance(value,list)):
#                 record_data=key
#             else:
#                 meta_data.append(key)
               
# elif(type(d)==dict):
#     for key,value in d.items():
#         if(isinstance(value,list)):
#             record_data=key
#         else:
#             meta_data.append(key)

# # print(meta_data,record_data)  
# #for subtasks
# if record_data=='':
#     record_data=None
  
    



