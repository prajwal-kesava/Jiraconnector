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

sprint_ids=[]
# print(board_ids)
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
Emptydf.to_csv("jira_csv/"+JSON_FILE+".csv",columns=['id','state','name','startDate','endDate','completeDate','originBoard','IDgoal'],index=False)
print(len(sprint_ids))
distinct_sprint_id = set()
uniq = [x for x in sprint_ids if x not in distinct_sprint_id and not distinct_sprint_id.add(x)]
print(len(distinct_sprint_id))
# {
#     'maxResults': 50, 'startAt': 0, 'total': 1, 'isLast': True, 
# 'values': [
#     {'id': 21, 'self': 'https://tapestrykpi.atlassian.net/rest/agile/1.0/board/21',
#  'name': 'VAT board', 'type': 'scrum',
#   'location': {
#      'projectId': 11800,
#   'displayName': 'Virgin Atlantic Tapestry (VAT)', 
#  'projectName': 'Virgin Atlantic Tapestry', 
#  'projectKey': 'VAT', 
#  'projectTypeKey': 'software', 
#  'avatarURI': '/secure/projectavatar?size=small&s=small&pid=11800&avatarId=11449',
#   'name': 'Virgin Atlantic Tapestry (VAT)'}
#  }
#  ]
#  }