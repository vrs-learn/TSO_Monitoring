from database import Database
from tsoapi import CDP_api
from statistics import mean
#from env_details import envDB

db=Database("tsohealth.db")

def read_db(server):
    data=db.select_query("select * from tsostats where stat_time >= datetime('now','-10 minute','localtime') and server='%s'" % server)
    #print("\nPrinting the Performance Metrics of TSO for Server"+str(server))
    #print("Server\t\tThreads\tMaximum_Memory\tTotal_Memory\tAvailable_Memory\tUsed_Memory\tVM_Uptime\t\tTime")
    #for row in data:
    #    print(str(row[1])+"\t"+str(row[2])+"\t"+str(row[3])+"\t\t"+str(row[4])+"\t\t"+str(row[5])+"\t\t\t"+str(row[6])+"\t\t"+str(row[7])+"\t"+str(row[8]))
    return data

def populate_adapter_details(adapters_list,grid_adapters):
    grid_adapter_details = []
    for adapter in adapters_list :
        for x in grid_adapters :
            if x['name']==adapter:
                grid_adapter_details.append(x)
    return grid_adapter_details

def form_adapter_body(adapter_details):
    adapter_body=[]
    for x in adapter_details:
        temp={}
        temp['name']=x['name']
        temp['version']=x['version']
        temp['revision']=x['revision']
        temp['peerName']=x['status'][0]['peerName']
        adapter_body.append(temp)
    return adapter_body

def filter_active_adapters(adapters_list,filter_state):
    filtered_adapters=[]
    for adap in adapters_list:
        get_status=adap['status'][0]['status']
        if get_status != filter_state :
            filtered_adapters.append(adap)
        else :
            print("Adapter "+adap['name']+" is "+get_status+"\n")
    return filtered_adapters

def check_metrics_data(grid_details):
    for grid in grid_details :
        if len(grid['details']) == 0 :
            return "blank"
            break
        else :
            return "exist"

def get_max_load(grid_ratios):
    list_avail_threads=[]
    for x in grid_ratios:
        list_avail_threads.append(x['avail_thread'])
    return min(list_avail_threads)

def get_ratios(grid_details):
    grid_ratios=[]
    for grid in grid_details:
        x={}
        x['cdpname']=grid['cdpname']
        x['server']=grid['server']
        x['avg_thread']=int(mean(list(zip(*grid['details']))[2]))
        x['avg_used_mem']=int(mean(list(zip(*grid['details']))[6]))
        x['avg_free_mem']=int(mean(list(zip(*grid['details']))[5]))
        x['mem_per_thread']=int(x['avg_used_mem'] / x['avg_thread'])
        x['avail_thread']=int(x['avg_free_mem'] / x['mem_per_thread'])
        grid_ratios.append(x)
    max_load=get_max_load(grid_ratios)
    for grid in grid_ratios:
        grid.update({'ratio_factor':int(grid['avail_thread'] / max_load)})
        print(grid_ratios)
    return grid_ratios

#############################################
################## M A I N ##################
#############################################

list_of_grid=[{'cdpname' : 'PROD1' , 'server' : 'clm-aus-018787'}, {'cdpname' : 'PROD2' , 'server' : 'clm-aus-018786'}]
list_of_adapters=['FileAdapter']

'''
grid1_cdp=CDP_api("http://clm-aus-018787:38080","aoadmin","admin123")
grid2_cdp=CDP_api("https://clm-aus-018786:38080","aoadmin","admin123")
grid1_cdp.login()
grid2_cdp.login()
'''

grid_cdp_details=[]
for grid in list_of_grid:
    grid_d={}
    grid_d['cdpname']=grid['cdpname']
    grid_d['server']=grid['server']
    grid_d['details']=read_db(grid['server'])
    grid_cdp_details.append(grid_d)

#print(grid_cdp_details)

if check_metrics_data(grid_cdp_details) == 'exist' :
    ratios=get_ratios(grid_cdp_details)
    pool=[]
    for ratio in ratios:
        #print("Ratio for "+ratio['cdpname']+" is : "+str(ratio['ratio_factor']))
        for i in range(ratio['ratio_factor']):
            pool.append(ratio['cdpname'])
    print("The final Pool is : "+str(pool))
else:
    print("Sorry !! Threads Data Unavailable to take any action")
