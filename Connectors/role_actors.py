import json
import pandas as pd
import os
import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
from pandas.io.json import json_normalize
cp= ConfigParser()
from pprint import pprint
cp.read( r"jiraprop.ini" )
JIRA_EMAIL = cp.get('user details','user')
JIRA_TOKEN = cp.get('user details','apikey')
BASE_URL = cp.get('user details','URL')
API_END_URL=cp.get('END URL','role_actors')
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
respone_data=api_call(API_URL,HEADERS,BASIC_AUTH)
data=json.loads(respone_data)
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
with open("jira_json/"+JSON_FILE+".json",'w',encoding='utf-8') as f:
	json.dump(data, f, ensure_ascii=False, indent=4)
lst=[]
df=pd.DataFrame()
print(type(df))
for role in data:
	for key,value in role.items():
		if(key=='actors'):
			if(isinstance(value,list)):
    				lst.append(role['id'])
for i in range(len(lst)):
	#print(lst[i])
	API_URL_END_2=API_URL+"/"+str(lst[i])+"/actors"		
	print(API_URL_END_2)
	response=api_call(API_URL_END_2,HEADERS,BASIC_AUTH)
	data=json.loads(response)
	#print(data)
	work_data=json_normalize(data,record_path='actors',errors='ignore',sep='_')
	df=df.append(work_data,ignore_index=True,sort=True)

df.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','displayName','name','type'],index=False)



