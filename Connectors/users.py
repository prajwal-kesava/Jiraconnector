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
API_END_URL=cp.get('END URL','users')
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
data=json.loads(response_data)
print(data)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
	json.dump(data, f, ensure_ascii=False, indent=4)

account_ids=[]
for id in data:
    account_ids.append(id['accountId'])

print(account_ids)

# response=api_call(BASE_URL+"/rest/api/3/"+"user?username=durgadevi.t",HEADERS,BASIC_AUTH)
# data=json.loads(response)
# with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
# 	json.dump(data, f, ensure_ascii=False, indent=4)
df=pd.DataFrame()
for id in account_ids:
    API_URL=BASE_URL+"/rest/api/3/user?accountId="+id
    print(API_URL)
    response=api_call(API_URL,HEADERS,BASIC_AUTH)
    data=json.loads(response)
    work_data=json_normalize(data,errors='ignore',sep='_')
    df=df.append(work_data,ignore_index=True,sort=True)
df.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['accountId','avatarUrls_48x48','displayName','emailAddress','key','name','self','timeZone'],index=False)

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
  
    



