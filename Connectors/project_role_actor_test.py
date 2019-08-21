import pandas as pd
from projectkeys import project_not_archived_ids as pk_id
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
role_data=json.loads(response_data)
# print(d)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
print(JSON_FILE)
# with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
# 	json.dump(d, f, ensure_ascii=False, indent=4)

# with open(JSON_FILE+".json") as f:
#     d=json.load(f)
roles_id=[]
project_id=[]
for role in role_data:
    	for key,value in role.items():
    			if(key=='actors'):
    					if(isinstance(value,list)):
    							roles_id.append(role['id'])



print(roles_id) 
 

# actor_id=[]
# response_data_actor=api_call("https://tapestrykpi.atlassian.net/rest/api/3/role",HEADERS,BASIC_AUTH)
# data_actor=json.loads(response_data_actor)
# # print(type(df))
# for role in data_actor:
# 	for key,value in role.items():
# 		if(key=='actors'):
# 			if(isinstance(value,list)):
#     				actor_id.append(role['id'])
# print(actor_id)

API_URL="https://tapestrykpi.atlassian.net/rest/api/3/project/"

df=pd.DataFrame()
# pk_id=pk_id("12442")
# ls=[]
# ls.append(pk_id)
print(type(pk_id))

for i in pk_id:
	for j in roles_id:
    		
		API_URL_END_2 = API_URL +str(i) + "/role/" + str(j)
		print(API_URL_END_2)
		response = api_call(API_URL_END_2, HEADERS, BASIC_AUTH)
		data = json.loads(response)
		key='actors'
		if key in data.keys():
		
			work_data = json_normalize(data, record_path = 'actors', errors = 'ignore', sep = '_')
			work_data['project_id'] = i
			work_data['role_id'] = j# role_prj = pd.concat([w, work_data], axis = 1)
			df = df.append(work_data, ignore_index = True, sort = True)
df=df.dropna(thresh=3)
df.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','project_id','role_id','displayName','name','avatarUrl','actorUser_accountId'],index=False)


