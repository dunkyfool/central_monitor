import json
from pprint import pprint

CURL_PATH = '../conf/grafana_dashboard_template/curl/'
UI_PATH = '../conf/grafana_dashboard_template/UI/'
FILE_LIST = ['page_one.json','miner_status.json']

def loadJSON(name):
    curl = json.load(open(CURL_PATH+name))
    ui   = json.load(open(UI_PATH+name))
    return curl, ui

def switch_panel():
    for name in FILE_LIST:
        curl, ui = loadJSON(name)
        curl['dashboard']['panels'] = ui['panels']
        with open(CURL_PATH+name,'w') as f:
            json.dump(CURL_PATH+name, f)

if __name__=="__main__":
    switch_panel()
