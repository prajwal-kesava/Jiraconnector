import pandas as pd
import os
from projectkeys import project_not_archived_ids as pk_id
import string
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
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]
def api_call(url,header,authentication):
    response = requests.get(
    url,
    headers=header,
    auth=authentication
    )
    return response.text



                       
Emptydf=pd.DataFrame()
emp=pd.DataFrame()
board_ids=[]
for id in pk_id:
    API_URL_END=API_URL+id
    print(API_URL_END)
    respone_data=api_call(API_URL_END,HEADERS,BASIC_AUTH)
    data=json.loads(respone_data)

    for key,value in data.items():
        if(key=='values'):
            for v in value:
                name_board=v['name']
                name='Scrum'
                if name in name_board:
                    board_ids.append(v['id'])

# print(board_ids)
sprint_ids=[]

for board_id in board_ids:
    API_URL_END="/rest/agile/1.0/board/"
    API_URL=BASE_URL+API_URL_END+str(board_id)+"/sprint"
    print(API_URL)
    response_data=api_call(API_URL,HEADERS,BASIC_AUTH)
    data=json.loads(response_data)
    work_data=json_normalize(data,record_path='values',errors='ignore',sep='_')
    Emptydf=Emptydf.append(work_data,ignore_index=True,sort=True)
print(Emptydf.columns)  
sprint_ids=list(Emptydf['id'])
# Emptydf.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','state','name','startDate','endDate','completeDate','originBoard','IDgoal'],index=False)
print(len(sprint_ids))
distinct_sprint_ids = set()
uniq = [x for x in sprint_ids if x not in distinct_sprint_ids and not distinct_sprint_ids.add(x)]
print(len(distinct_sprint_ids))
# GET /rest/agile/1.0/board/{boardId}/sprint/{sprintId}/issue
df=pd.DataFrame()
for b_id in board_ids:
    for s_id in distinct_sprint_ids:
        API_END_URL="/rest/agile/1.0/board/"+str(b_id)+"/sprint/"+str(s_id)+"/issue"
        API_URL=BASE_URL+API_END_URL
        print(API_URL)
        response=api_call(API_URL,HEADERS,BASIC_AUTH)
        data=json.loads(response)
        # print(data)
        work_data=json_normalize(data,errors='ignore',record_path='issues',sep="_")
        work_data['originBoardID']=b_id
        work_data['sprint_id']=s_id
        df=df.append(work_data,ignore_index=True,sort=True)
df.to_csv('jira_csv/'+JSON_FILE+".csv",columns=['sprint_id','originBoardID','total','id','key'],index=False)







