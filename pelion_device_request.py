#!/usr/bin/env python3

import argparse
import base64
import sys
import time
import requests


def main():
    print("Starting Pelion requests")
    # command line
    parser = argparse.ArgumentParser(description="Pelion device interactions")
    parser.add_argument("-a", "--apikey", type=str, help="User api key")
    parser.add_argument("-d", "--device_ID", type=str, help="Pelion device_ID (endpoint)", default="*")
    parser.add_argument("-m", "--method", type=str, help="method to device resource", default="GET")
    #smaple app increasing counter
    parser.add_argument("-r", "--resource", type=str, help="device resource uri", default="/3200/0/5501")
    parser.add_argument("-p", "--payload", type=str, help="method payload (to put/post)", default="0")
    parser.add_argument("-i", "--interval", type=str, help="interval for re-doing", default="0")

    options = parser.parse_args()

    if (options.apikey is None):
        parser.print_help()
        return 1
    print("Create session")
    session = requests.Session()

    auth="Bearer "+options.apikey
    extheaders = {'Authorization': auth}
    extheaders['Connection'] = 'keep-alive'
    extheaders['Content-type'] = 'application/json'

    pelion_url = "https://api.us-east-1.mbedcloud.com/v2/device-requests/"

    print("Making requst: %s" %options.method, options.device_ID, options.resource, options.payload)
    '''async_request
    POST /v2/device-requests/DEVICE_ID?async-id=_NNN_

    { "method": "GET", "uri": "/5/0/1" }
    
    { "method": "PUT", "uri": "/5/0/1", "accept": "text/plain", "content-type": "text/plain", "payload-b64": "dmFsdWUxCg==" }
    
     execute
    { "method": "POST", "uri": "/123/1/1" }
    '''
    payload={}
    payload['method'] = options.method
    payload['uri'] = options.resource
    if (options.method !="put" or options.method =="PUT"):
        #payload['accept']= "text/plain"
        payload['content-type']= "text/plain"
        ''' example
        message = "Python is fun"        
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        '''
        payload['payload-b64'] = base64.b64encode(options.payload.encode('ascii')).decode('ascii')

    asyncid=str(time.time()).replace('.','-')
    print("ASYNCID "+asyncid)
    url=pelion_url+str(options.device_ID)+'?async-id='+asyncid
    #check and break the interval later
    while(True):

        #POST TO PELION, device method in JSON
        resp = session.post(url, headers=extheaders, json=payload)

        if resp.status_code < 400:
            print("HTTP OK :"+ str(resp.status_code))
            print("\t "+str(resp.text))
        else:
            print("HTTP ERROR :" + str(resp.status_code))
            print("\t " + str(resp.reason))
            print("\t " + str(resp.text))

        if int(options.interval) > 0:
            print("sleep "+str(options.interval))
            time.sleep(float(options.interval))
        else:
            print("done")

            return 0

if __name__ == "__main__":
    sys.exit(main())