#!/usr/bin/env python3

import argparse
import base64
import sys
import time
import asyncio
import websockets
import json
import requests

def main():
    asyncio.get_event_loop().run_until_complete(listen())

def cleartext(content):
    payload = getItem('payload', content)
    if payload is None: return
    clear = base64.b64decode(payload)
    print("\t\t payload clear-text str length: " + (str(len(clear))))
    print("\t\t payload clear-text: " + str(clear, errors='ignore'))


def getItems(key,content):
    list=[]
    try:
        list=content[key]
    except KeyError:
        list=[]
    return list

def getItem(key, content):
    try:
        val=content[key]
    except KeyError:
        return None
    return val

async def process(data):
    content = json.loads(data)
    keys=['notifications','async-responses','registrations','reg-updates']

    for key in keys:
        items=getItems(key, content)
        if len(items) > 0:
            print(key.upper())
            for item in items:
                print("\t " + str(item))
                #print payload if there for notif, async-resp
                if ( key == keys[0] or key == keys[1] ):
                    cleartext(item)
                else:
                    ep=getItem('ep', item)
                    if ep is not None:print("\tEP "+str(ep))

async def listen():
    print("Starting Pelion WebSocket for notifications")
    # command line
    parser = argparse.ArgumentParser(description="Pelion device interactions")
    parser.add_argument("-a", "--apikey", type=str, help="User api key")
    parser.add_argument("-d", "--device_ID", type=str, help="Pelion device_ID (endpoint)", default="*")
    parser.add_argument("-r", "--resource", type=str, help="device resource to subscribe, empty means all", default="")

    options = parser.parse_args()

    if (options.apikey is None):
        parser.print_help()
        sys.exit(1)
    print("Create session")
    session = requests.Session()

    auth = "Bearer " + options.apikey
    extheaders = {'Authorization': auth}

    pelion_url = "https://api.us-east-1.mbedcloud.com/v2/"

    print("Clear previous subscriptions")
    url = pelion_url + "subscriptions"

    resp = session.delete(url, headers=extheaders)
    print("HTTP " + str(resp.status_code))
    if resp.status_code >= requests.codes.bad:
        exit(1)

    print("New subscription to ep: %s" % options.device_ID, options.resource)
    # trickery, json is
    # [
    #        {
    #          "endpoint-name": "node-001",
    #          "resource-path": ["/dev"]
    #        },
    #       {
    #          "endpoint-name": "node*"
    #       }
    # ]
    payload = []
    item = {}
    if (len(options.resource) > 0):
        item['endpoint-name'] = options.device_ID
        respath = []
        respath.append(options.resource)
        item['resource-path'] = respath
        payload.append(item)
    else:
        item['endpoint-name'] = options.device_ID
        payload.append(item)
    resp = session.put(url, headers=extheaders, json=payload)
    print("HTTP " + str(resp.status_code) + str(resp.text))
    if resp.status_code >= requests.codes.bad:
        exit(1)

    print("Register websocket")
    #no niceties, no payload configuiration
    url = pelion_url + "notification/websocket"
    resp = session.put(url, headers=extheaders)

    print("HTTP " + str(resp.status_code) + str(resp.text))
    if resp.status_code >= requests.codes.bad:
        exit(1)

    print("connect websocket")
    ws_url = "wss://api.us-east-1.mbedcloud.com/v2/notification/websocket-connect"
    async with websockets.connect(ws_url, extra_headers=extheaders) as websocket:

        while(True):
            data = await websocket.recv()
            await process(data)


if __name__ == "__main__":
    main()
    sys.exit(0)