import pandas as pd 
from projectKeys import project_not_archived_ids as pid
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
BASE_URL = cp.get('user details','server')
JSON_FILE=os.path.splitext(os.path.basename(__file__))[0]

# API_END_URL=cp.get('END URL','issues')
API_URL = "/rest/api/3/search"
API_URL = BASE_URL+API_URL+"?jql=project="
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
df=pd.DataFrame()
total=int(0)
for prj in pid:
    API_URL_END=API_URL+str(prj)+"&maxResults=1000"
    print(API_URL_END)
    response_data=api_call(API_URL_END,HEADERS,BASIC_AUTH)
    data=json.loads(response_data)
    total=total+int(data['total'])
    work_data=json_normalize(data,record_path='issues',errors='ignore',sep='_')
    df=df.append(work_data,ignore_index=True,sort=True)
df.to_csv(JSON_FILE+".csv",columns=['id','key','fields_issuetype_id','fields_issuetype_name','fields_issuetype_subtask','fields_priority_id','fields_priority_name','fields_project_id','fields_project_key','fields_project_name','fields_assignee_accountId','fields_assignee_active','fields_assignee_displayName','fields_project_projectCategory_id','fields_project_projectCategory_name','fields_project_projectTypeKey','fields_project_self','fields_assignee_emailAddress','fields_assignee_key','fields_assignee_name','fields_assignee_timeZone','fields_created','fields_creator_accountId','fields_creator_active','fields_creator_displayName','fields_creator_emailAddress','fields_creator_key','fields_creator_name','fields_creator_timeZone','fields_reporter_accountId','fields_reporter_accountType','fields_reporter_active','fields_reporter_displayName','fields_reporter_emailAddress','fields_reporter_key','fields_reporter_name','fields_reporter_timeZone','fields_status_description','fields_status_id','fields_status_name','fields_status_statusCategory_id','fields_status_statusCategory_key','fields_status_statusCategory_name','fields_statuscategorychangedate','fields_summary','fields_timeestimate','fields_timeoriginalestimate','fields_timespent','fields_timetracking_originalEstimate','fields_timetracking_originalEstimateSeconds','fields_timetracking_remainingEstimate','fields_timetracking_remainingEstimateSeconds','fields_timetracking_timeSpent','fields_timetracking_timeSpentSeconds','fields_updated'],index=False)

print(total)

