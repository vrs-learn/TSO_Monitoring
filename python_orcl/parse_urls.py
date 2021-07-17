import requests
import time
from bs4 import BeautifulSoup as bs
from database import Database
import sys
import re

def get_content(url):
    try :
        url_req=requests.get(url,verify=False)
        return url_req.status_code , url_req.content
    except :
        return 400 , ""

def save_info(params,server):
    db=Database("tsohealth.db")
    db.insert(server,params['Active Threads'],params['Maximum Memory'],params['Total Memory'],params['Available Memory'],params['Used Memory'],params['VM Uptime'])

def collect_info(content,server):
    grid_info={}
    items=[]
    values=[]
    soup=bs(content,'html.parser')
    rows=soup.find(id="system-metric-view:menu").find_all('tr')
    for row in rows[0].find_all('td'):
        items.append(row)
    for row in rows[1].find_all('td'):
        values.append(row)
    for item, value in zip(items, values):
        if re.search(r'Memory',item.string):
            if re.search(r'MB',value.string):
                grid_info[item.string]=int(re.match(r'(\w*)\s*(MB)',value.string).groups()[0])
            elif re.search(r'GB',value.string):
                val=int(re.match(r'(\w*)\s*(GB)',value.string).groups()[0])*1024
                grid_info[item.string]=val
            else:
                print("Data from the Grid URL is not returning valid Units of Memory. Exiting")
                sys.exit(2)
        else :
            grid_info[item.string]=value.string
        #grid_info.append(x)
    print(grid_info)
    save_info(grid_info,server)

if __name__=="__main__":
    while True:
        server_list=[{'server':"clm-aus-018786" , 'url':"https://clm-aus-018786:38080"} , {'server':"clm-aus-018787" , 'url':"http://clm-aus-018787:38080"}, {'server':"clm-pun-027160" , 'url':"http://clm-pun-027160:38080"}]
        for x in server_list:
            server=x['server']
            cdp_url=x['url']
            grid_info_url=cdp_url+"/baocdp/console/gridList.jsf"
            status, content = get_content(grid_info_url)
            if status == 200:
                collect_info(content,server)
            else:
                print("Unable to connect to the URL "+grid_info_url+". Error Code "+str(status))
                #sys.exit(1)
        time.sleep(15)
