# # import pandas as pd
# # import json
# # import requests
# # from requests.auth import HTTPBasicAuth
# # from configparser import ConfigParser
# # from pandas.io.json import json_normalize
# # cp= ConfigParser()
# # cp.read( r"jiraprop.ini" )
# # JIRA_EMAIL = cp.get('user details','user')
# # JIRA_TOKEN = cp.get('user details','apikey')
# # BASE_URL = cp.get('user details','URL')
# # API_END_URL=cp.get('END URL','role_actors')
# # API_URL = "/rest/api/3/"+API_END_URL
# # API_URL = BASE_URL+API_URL
# # print(API_URL)
# # BASIC_AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
# # HEADERS = {'Content-Type' : 'application/json;charset=iso-8859-1'}
# # def api_call(url,header,authentication):
# #     response = requests.get(
# #     url,
# #     headers=header,
# #     auth=authentication
# #     )
# #     return response.text
# # response_data=api_call(API_URL,HEADERS,BASIC_AUTH)
# # d=json.loads(response_data)
# # print(d)
# # JSON_FILE="role_actor"
# # # with open(JSON_FILE+".json",'w',encoding='utf-8') as f:
# # # 	json.dump(data, f, ensure_ascii=False, indent=4)

# # # with open(JSON_FILE+".json") as f:
# # #     d=json.load(f)

# # # meta_data=[]
# # # record_data=''

# # # # print(type(d))
# # # if(type(d)==list):
# # #     for li in d:
# # #         for key,value in li.items():
# # #             if(isinstance(value,list)):
# # #                 record_data=key
# # #             else:
# # #                 meta_data.append(key)
               
# # # elif(type(d)==dict):
# # #     for key,value in d.items():
# # #         if(isinstance(value,list)):
# # #             record_data=key
# # #         else:
# # #             meta_data.append(key)

# # # # print(meta_data,record_data)  
# # # #for subtasks
# # # if record_data=='':
# # #     record_data=None
  
    
# # work_data=json_normalize(data=d,record_path='actors',sep="_")
# # work_data.to_csv("jira_csv/"+JSON_FILE+".csv",index=False)

# import pandas as pd

# # df=pd.read_csv('jira_csv/test2.csv')
# # df=df.dropna()
# # df.to_csv('jira_csv/test7.csv')
# def looping(l):
#     w=pd.DataFrame({'name':'hsg','id':'jsb'},index=[0])
#     for i in range(l):
#         w=w.append(w)
                
#     return w

# dataa=looping(10)
# print(dataa)
        
from projectkeys import project_not_archived_ids as pk_id
print(pk_id)

# print(prj_id.project_not_archived_ids)

print('hello@me'.split('@')[0])