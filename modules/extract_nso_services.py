from modules.nso import NSO
from modules.ssh import Tunnel

def nso_raw(endpoint_type):
#    def save_response(nso_handler, endpoint_type):
    #for endpoint_type in nso_endpoints:
    print("Creating SSH DYNAMIC TUNNEL...")
    tunnel_handler = Tunnel()
    print("Done Creating SSH DYNAMIC TUNNEL...")
    nso_handler = NSO()
    if nso_handler.get(endpoint_type,'l2vpn') != 500:
        if '/vpn' in endpoint_type:
            response = nso_handler.get(endpoint_type, 'l3vpn')
            # response = response.json()
            file = open("l3vpn_vpn.json", "w")
            file.write(response.text)
            file.close()
        elif '/link' in endpoint_type:
            response = nso_handler.get(endpoint_type, 'l3vpn')
            # response = response.json()
            file = open("l3vpn_link.json", "w")
            file.write(response.text)
            file.close()
        elif 'l2vpn' in endpoint_type:
            response = nso_handler.get(endpoint_type, 'l2vpn')
            # response = response.json()
            file = open("l2vpn.json", "w")
            file.write(response.text)
            file.close()
        tunnel_handler.disconnect()
        return('Raw files created please')
    else:
        return 'NSO Busy please try again!!'