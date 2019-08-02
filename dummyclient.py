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

username = "agent1"
password = ""
uuid = "6817ca74-4e23-4e16-a004-feae757a45c0"
url = "http://localhost:8000"
server1 = "066182e8-e56b-40a8-8ee9-d92dce71e07e"
server2 = "6e2a72bf-b5d1-4d32-ac83-8f6cd035d28e"
server3 = "86023348-270a-4c94-bdac-877defdb17c6"


data_point = {
    "uuid": uuid,
    "test_type": "RFC6349",
    "network": "dsl",
    "pcap": "sample.pcap",
    "lat": random.uniform(12, 13),
    "long": random.uniform(120, 122),
    "mode": random.choices(['normal', 'reverse', 'bidirectional', 'simultaneous'])[0],
    "results": {
        "set1": {
            "ts": datetime.now(),   # TODO: add timezone information, or assume that clients will always send in UTC
            "server": random.choices([server1, server2, server3])[0],
            "direction": random.choices(['forward', 'reverse'])[0],
            "path_mtu": random.randint(1400, 1500),
            "baseline_rtt": random.uniform(1, 1000),
            "bottleneck_bw": random.uniform(1, 10000000000),
            "bdp": random.uniform(1, 10000000000),
            "min_rwnd": random.uniform(1, 65000),
            "ave_tcp_tput": random.uniform(1, 10000000000),
            "ideal_tcp_tput": random.uniform(1, 10000000000),
            "actual_transfer_time": random.uniform(1, 100),
            "ideal_transfer_time": random.uniform(1, 100),
            "tcp_ttr": random.uniform(0,1),
            "trans_bytes": random.uniform(1, 10000000000),
            "retrans_bytes": random.uniform(1, 10000000000),
            "tcp_eff": random.uniform(1, 100),
            "ave_rtt": random.uniform(1, 1000),
            "buffer_delay": random.uniform(1, 10000000000),
        },
        "set2": {
            "ts": datetime.now(),   # TODO: add timezone information, or assume that clients will always send in UTC
            "server": random.choices([server1, server2, server3])[0],
            "direction": random.choices(['forward', 'reverse'])[0],
            "path_mtu": random.randint(1400, 1500),
            "baseline_rtt": random.uniform(1, 1000),
            "bottleneck_bw": random.uniform(1, 10000000000),
            "bdp": random.uniform(1, 10000000000),
            "min_rwnd": random.uniform(1, 65000),
            "ave_tcp_tput": random.uniform(1, 10000000000),
            "ideal_tcp_tput": random.uniform(1, 10000000000),
            "actual_transfer_time": random.uniform(1, 100),
            "ideal_transfer_time": random.uniform(1, 100),
            "tcp_ttr": random.uniform(0, 1),
            "trans_bytes": random.uniform(1, 10000000000),
            "retrans_bytes": random.uniform(1, 10000000000),
            "tcp_eff": random.uniform(1, 100),
            "ave_rtt": random.uniform(1, 1000),
            "buffer_delay": random.uniform(1, 10000000000),
        },
    }
}

creds = {
    "username": username,
    "password": password,
    "uuid": uuid # agent uuid
}
try:
    # Request for Agent token
    r = requests.post(url=url+"/api/register", data=creds)
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
    r = requests.post(url+"/api/submit",
                      headers=headers,
                      data=data_json,
                      timeout=30)

except Exception as e:
    print("ERROR: %s." % e)

if r.status_code == 200:
    print("Submit success!")
else:
    print("Exiting due to status code %s: %s" % (r.status_code, r.text))
