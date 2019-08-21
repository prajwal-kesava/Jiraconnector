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
API_END_URL=cp.get('END URL','project_role')
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
# print(data)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
	json.dump(data, f, ensure_ascii=False, indent=4)


lst=[]
df=pd.DataFrame()
print(type(df))
for project in data:
    lst.append(project['id'])
print(lst)
for i in range(len(lst)):
	#print(lst[i])
	# URL-->https://tapestrykpi.atlassian.net/rest/api/3/project/{projectIdOrKey}/role
	API_URL_END_2=API_URL+"/"+str(lst[i])+"/role"		
	print(API_URL_END_2)
	response=api_call(API_URL_END_2,HEADERS,BASIC_AUTH)
	data=json.loads(response)
	# print(data)
    # with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
	# 	json.dump(data, f, ensure_ascii=False, indent=4)
for roles in data.keys():
    	print(roles)
    		
work_data=json_normalize(data,errors='ignore',sep='_')
# df=df.append(work_data,ignore_index=True,sort=True)
print(work_data)
    

work_data.to_csv("jira_csv/"+JSON_FILE+".csv",index=False)

