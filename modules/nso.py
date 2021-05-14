from decouple import config
import requests
from modules.request_status import status
import json
import re

class NSO:

    def get(self,endpoint,_type="l2vpn"):
        NSO_URL = config("NSO_URL")

        url = f'{NSO_URL}{endpoint}'
        
        headers = {
            'Content-type': 'application/vnd.yang.data+json',
            'Accept': 'application/vnd.yang.data+json' if _type.lower() == "l2vpn" else "application/vnd.yang.collection+json",
        }
        if status[0] == 1:
            response = 500
        elif status[0] == 0:
            with open('/vagrant/parser_api/modules/request_status.py', 'w') as myrequest:
                myrequest.write("status=[1]")
            print("Sending Request...")
            response = requests.request(\
                "GET"\
                ,url\
                ,headers=headers\
                ,proxies={"http":config("NSO_PROXY"),"https:":config("NSO_PROXY")}\
                ,auth = (config("NSO_USERNAME"),config("NSO_PASSWORD"))\
            )
            with open('/vagrant/parser_api/modules/request_status.py', 'w') as myrequest:
                myrequest.write("status=[0]")
        return response


