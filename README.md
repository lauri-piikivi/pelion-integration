# pelion-integration
simple python scripts for Pelion IoT platform usage/integration https://www.pelion.com/docs/device-management/current/service-api-references/using-the-apis.html

Minimal device amounts, no fancies yet 

Tested on python3 only

REQUIRES Python libraries
- requests
- asyncio
- websockets


Sample output of Pelion notifications

'''
subscription to ep: 01722bd4d07d0000000000010012408a
HTTP 204
Register websocket
HTTP 200{"status":"unknown","queue_size":-1}
connect websocket
REGISTRATIONS
	 {'ep': '01722bd4d07d0000000000010012408a', 'original-ep': 'test_dev_01', 'ept': 'default', 'resources': [{'path': '/3/0/13', 'obs': True}, {'path': '/3/0/21', 'obs': True}, {'path': '/3/0/18', 'obs': True}, {'path': '/3/0/17', 'obs': True}, {'path': '/3/0/2', 'obs': True}, {'path': '/3/0/1', 'obs': True}, {'path': '/3/0/0', 'obs': True}, {'path': '/3/0/5', 'obs': False}, {'path': '/3/0/16', 'obs': True}, {'path': '/3/0/11', 'ct': 'application/vnd.oma.lwm2m+tlv', 'obs': True},...}
	
  EP 01722bd4d07d0000000000010012408a
  
...

NOTIFICATIONS
	 {'ep': '01722bd4d07d0000000000010012408a', 'path': '/3200/0/5501', 'ct': 'text/plain', 'payload': 'OQ==', 'max-age': 0}
		 payload clear-text str length: 1
		 payload clear-text: 9

NOTIFICATIONS
	 {'ep': '01722bd4d07d0000000000010012408a', 'path': '/3200/0/5501', 'ct': 'text/plain', 'payload': 'MTA=', 'max-age': 0}
		 payload clear-text str length: 2
		 payload clear-text: 10

ASYNC-RESPONSES
	 {'id': '1589874198-210669', 'status': 200, 'payload': '', 'max-age': 60}
		 payload clear-text str length: 0
		 payload clear-text:

NOTIFICATIONS
	 {'ep': '01722bd4d07d0000000000010012408a', 'path': '/3200/0/5501', 'ct': 'text/plain', 'payload': 'MA==', 'max-age': 0}
		 payload clear-text str length: 1
		 payload clear-text: 0
'''
