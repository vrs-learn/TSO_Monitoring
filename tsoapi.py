import requests
import json
import sqlite3
import getpass

class CDP_api:

    def __init__(self, url, user, passw):
        self.url=url
        self.login_url=self.url+"/baocdp/rest/login"
        self.logout_url=self.url+"/baocdp/rest/logout"
        self.header={"username" : user, "password" : passw}
        requests.packages.urllib3.disable_warnings()

    def login(self):
        try :
            self.login_r=requests.post(self.login_url, json=self.header,verify=False)
            self.login_status_code=self.login_r.status_code
            if self.login_status_code == 200:
                self.auth_token=self.login_r.headers['Authentication-Token']
            else :
                self.auth_token=""
        except :
            print("Connection unavailable.")
            self.login_r=""
            self.login_status_code=""
            self.auth_token=""

    def logout(self):
        self.logout_header = { "Authentication-Token" : self.auth_token }
        self.logout_r = requests.post(self.logout_url,headers=self.logout_header,verify=False)

    def get_active_modules(self):
        self.get_active_mod_header={ "Authentication-Token" : self.auth_token }
        self.get_active_mod_url=self.url+"/baocdp/rest/module?pattern=^[a-zA-Z0-9_-]{1,50}"
        self.get_active_mod_req=requests.get(self.get_active_mod_url,headers=self.get_active_mod_header,verify=False)
        self.get_active_mod_datastore = json.loads(self.get_active_mod_req.text)

    def get_repo_modules(self):
        get_repo_modules_url=self.url+"/baocdp/rest/module?repo=true"
        get_repo_modules_header={ "Authentication-Token" : self.auth_token }
        self.get_repo_modules_req=requests.get(get_repo_modules_url,headers=get_repo_modules_header,verify=False)
        self.get_repo_modules_datastore=json.loads(self.get_repo_modules_req.text)

    def activate_module(self, module_list):
        activate_url=self.url+"/baocdp/rest/module/activate"
        activate_header={ "Authentication-Token" : self.auth_token }
        activate_req_body=[]
        for mod in module_list:
            x={}
            x={'name':mod['name'], 'version':mod['ver'], 'revision':"1"}
            activate_req_body.append(x)
        print(activate_req_body)
        self.activate_req=requests.post(activate_url,json={'modules':activate_req_body},headers=activate_header,verify=False)
        print("Activate Request status : ")
        print(self.activate_req.status_code)
        print(self.activate_req.text)

    def activate_module_config(self,config_json):
        act_mod_config_url=self.url+"/baocdp/rest/module/config"
        act_mod_config_header={ "Authentication-Token" : self.auth_token }
        self.act_mod_config_req=requests.post(act_mod_config_url,json=config_json,headers=act_mod_config_header,verify=False)

    def enable_adapter(self,adapter_json):
        enable_url=self.url+"/baocdp/rest/adapter/enable"
        enable_header={ "Authentication-Token" : self.auth_token }
        self.enable_req=requests.post(enable_url,json=adapter_json,headers=enable_header,verify=False)
        self.enable_req_msg=json.loads(self.enable_req.text)

    def disable_adapter(self,adapter_json):
        disable_url=self.url+"/baocdp/rest/adapter/disable"
        disable_header={ "Authentication-Token" : self.auth_token }
        self.disable_req=requests.post(disable_url,json=adapter_json,headers=disable_header,verify=False)
        self.disable_req_msg=json.loads(self.disable_req.text)
        
    def get_adapters(self):
        get_adapter_url=self.url+"/baocdp/rest/adapter"
        get_adapter_header={ "Authentication-Token" : self.auth_token , "configDataType" : "JSON"}
        self.adapter_req=requests.get(get_adapter_url,headers=get_adapter_header,verify=False)
        return json.loads(self.adapter_req.text)

#tso = Tso_api("http://clm-aus-018787:38080/baocdp")
#tso.login()
