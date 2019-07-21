"""
    dummyclient.py
    Quick python code for testing the results server API
    07-10-2019
"""

import requests
import json
import ast
from datetime import datetime
import random

username = ""
password = ""
uuid = ""

data_point = {
    "uuid": uuid,
    "test_type": "RFC6349",
    "network": "dsl",
    "pcap": "sample.pcap",
    "lat": "14.654929",
    "long": "121.064947",
    "results": {
        "set1": {
            "ts": datetime.now(),   # TODO: add timezone information, or assume that clients will always send in UTC
            "server": "6067d5166e5741bfb5f7d596649e6916",
            "rtt": random.randint(1, 1000),
            "upload": random.randint(1, 10000000000),
            "download": random.randint(1, 10000000000),
        },
        "set2": {
            "ts": datetime.now(),
            "server": "198208cbde9f4965b7cf1a14468c3f55",
            "rtt": random.randint(1, 1000),
            "upload": random.randint(1, 10000000000),
            "download": random.randint(1, 10000000000),
        },
        "set3": {
            "ts": datetime.now(),
            "server": "6077a99978634a9b81fcb040b3fce540",
            "rtt": random.randint(1, 1000),
            "upload": random.randint(1, 10000000000),
            "download": random.randint(1, 10000000000),
        }
    }
}

creds = {
    "username": username,
    "password": password,
    "uuid": uuid # agent uuid
}
try:
    # Request for Agent token
    r = requests.post(url="http://localhost:8000/api/register", data=creds)
except Exception as e:
    print(e)

if r.status_code != 200:
    print("Exiting due to status code %s" % r.status_code)
    quit()

mytoken = ast.literal_eval(r.text)['Token']
data_json = json.dumps(data_point, default=str)
status_len = len(data_json)

headers = {
    "Authorization": "Token %s" % mytoken,
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": str(status_len)
}

try:
    r = requests.post("http://localhost:8000/api/submit",
                      headers=headers,
                      data=data_json,
                      timeout=30)

except Exception as e:
    print("ERROR: %s." % e)

if r.status_code == 200:
    print("Submit success!")
else:
    print("Exiting due to status code %s" % r.status_code)

quit()