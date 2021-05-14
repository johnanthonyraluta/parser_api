from fastapi import FastAPI
from modules.nso import NSO
from modules.ssh import Tunnel
from modules.flat_json import json_to_csv
from modules.sqlalchemy_connect import sqlalc_conn
from sqlalchemy.types import String
from modules.extract_nso_services import nso_raw
from modules.sql_connect import sql_connection
from datetime import datetime
#from decouple import config
import os,pathlib
import time
import json
import pandas as pd
import csv

import uvicorn

app = FastAPI()

#output_file_path = "/vagrant/parser_api/files/"
output_file_path = "/mnt/c/Users/jraluta/nso_parser/parser_api/files/"
nso_endpoints = ['/api/running/mpls-l3vpn/vpn',
                 '/api/running/mpls-l3vpn/link',
                 '/api/running/mpls-l2vpn?deep']
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
@app.get("/")
def index():
    mypage = "Welcome to NSO Parser!"
    return mypage

@app.get("/raw")
def get_raw_files():
    for endpoint_type in nso_endpoints:
        nso_services = nso_raw(endpoint_type)
        return nso_services

@app.get("/parse/")
#C:\Users\jraluta\nrfu\parser_api\files\l3vpn_link.json
def parse_output():
    for endpoint_type in nso_endpoints:
        if '/vpn' in endpoint_type:
            df = pd.read_json(output_file_path + 'l3vpn_vpn.json')
            df = df['collection']['mpls-l3vpn:vpn']
            new_df = json_to_csv(df)
            for columns in new_df.columns:
                if 'operations' in columns:
                    new_df = new_df.drop([columns], axis = 1)
            new_df.insert(0,'collection-date',dt_string, allow_duplicates=False)
            #new_df.loc[0,'collection-date'] = dt_string
            new_df.to_csv(output_file_path + 'l3vpn_vpn.csv', index=False, header=True)
        elif '/link' in endpoint_type:
            #df = pd.DataFrame(response['collection']['mpls-l3vpn:link'])
            df = pd.read_json(output_file_path + 'l3vpn_link.json')
            df = df['collection']['mpls-l3vpn:link']
            new_df = json_to_csv(df)
            new_df.loc[new_df['routing.static.ipv4-routes.ipv4-prefixes.network-subnet'].notnull(), 'routing'] = 'static'
            new_df.loc[new_df['routing.bgp.peer-ipv4'].notnull(), 'routing'] = 'bgp'
            for columns in new_df.columns:
                if 'operations' in columns or 'route-filtering.route-policy.route-policy-actions.main-match-action.match-community-in'\
                        in columns:
                    new_df = new_df.drop([columns], axis = 1)
            new_df.insert(0, 'collection-date',dt_string, allow_duplicates=False)
            #new_df.loc[0,'collection-date'] = dt_string
            new_df.to_csv(output_file_path + 'l3vpn_link.csv', index=False, header=True)
        elif 'l2vpn' in endpoint_type:
            #df = pd.DataFrame(response['mpls-l2vpn:mpls-l2vpn']['l2-vpn'])
            df = pd.read_json(output_file_path +'l2vpn.json')
            df = df['mpls-l2vpn:mpls-l2vpn']['l2-vpn']
            new_df = json_to_csv(df)
            for columns in new_df.columns:
                if 'operations' in columns:
                    new_df = new_df.drop([columns], axis = 1)
            new_df.insert(0, 'collection-date',dt_string, allow_duplicates=False)
            #new_df.loc[0,'collection-date'] = dt_string
            new_df.to_csv(output_file_path + 'l2vpn.csv', index = False, header=True)
    return("File Parsed and Saved!")

@app.get("/sql")
def nso_sql_create():
    engine = sqlalc_conn()
    engine.execute('DROP TABLE IF EXISTS L2VPN;')
    engine.execute('DROP TABLE IF EXISTS L3VPN_LINK;')
    engine.execute('DROP TABLE IF EXISTS L3VPN_VPN;')
    df_l2vpn = pd.read_csv(output_file_path +'l2vpn.csv')
    df_l3vpn_link = pd.read_csv(output_file_path +'l3vpn_link.csv')
    df_l3vpn_vpn = pd.read_csv(output_file_path + 'l3vpn_vpn.csv')
    df_l2vpn.to_sql("L2VPN", con=engine,schema=None,if_exists='replace', index=False,chunksize=1000,dtype={col_name: String(255) for col_name in df_l2vpn})
    df_l3vpn_link.to_sql("L3VPN_LINK",schema=None, con=engine,if_exists='replace', index=False,chunksize=1000,dtype={col_name: String(255) for col_name in df_l3vpn_link})
    df_l3vpn_vpn.to_sql("L3VPN_VPN",schema=None, con=engine,if_exists='replace', index=False,chunksize=1000,dtype={col_name: String(255) for col_name in df_l3vpn_vpn})
    return ("Files saved to MySQL DB")
