"""
    dummyclient.py
    Quick python code for testing the results server API
    07-10-2019
"""

import ast
import json
import pytz
import random
import requests

from datetime import datetime

# account variables
staff = "staff1"
staffpwd = "staff1"
agent = "newagent"
agentpwd = "newagent"
agent_uuid = ""
url = "http://localhost:8000"

# server uuids
server1 = ""
server2 = ""
server3 = ""

# client device hash
hashh = ""

# REGISTER CLIENT DEVICE

payload = {
    "hash": hashh
}
try:
    userauth = requests.auth.HTTPBasicAuth(staff, staffpwd)
    r = requests.post(
        url=url + "/api/register",
        auth=userauth,
        data=payload
    )
except Exception as e:
    print("Exiting due to status code %s: %s" % (r.status_code, r.text))

if r.status_code != 200:
    print("Exiting due to status code %s: %s" % (r.status_code, r.text))
    quit()

# GET TOKEN

payload = {
    "uuid": agent_uuid,
    "hash": hashh
}
try:
    userauth = requests.auth.HTTPBasicAuth(agent, agentpwd)
    r = requests.post(
        url=url + "/api/gettoken",
        auth=userauth,
        data=payload
    )
except Exception as e:
    print("Exiting due to status code %s: %s" % (r.status_code, r.text))

if r.status_code != 200:
    print("Exiting due to status code %s: %s" % (r.status_code, r.text))
    quit()


# SUBMIT DATA

data_point = {
    "uuid": agent_uuid,
    "test_type": "RFC6349",
    "network": "dsl",
    "pcap": "sample.pcap",
    "lat": random.uniform(12, 13),
    "long": random.uniform(120, 122),
    "mode": random.choices(['normal', 'reverse', 'bidirectional', 'simultaneous'])[0],
    "hash": hashh,
    "results": {
        "set1": {
            "ts": pytz.utc.localize(datetime.utcnow()),
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
            "ts": pytz.utc.localize(datetime.utcnow()),
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
