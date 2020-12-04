import subprocess
#import subprocess
import pprint
import json
import os
results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=BSSID"])

results = results.decode("ascii") # needed in python 3
results = results.replace("\r","")
ls = results.split("\n")

ls = ls[4:]
ssids = []
obj = {}
objs = []

if os.path.exists("wifi.json"):
    fh = open("wifi.json", "r+")
else:
    fh = open("wifi.json", "w+")
data = {}
if len(fh.read()) > 0:
    fh.seek(0)
    data = json.loads(fh.read())


x = 0
while x < len(ls):
    kv = ls[x].split(":")
    if ls[x].startswith("    Encryption"):
        obj["Encryption"] = kv[-1].strip()

    if ls[x].startswith("SSID"):
        if not ls[x].startswith("SSID 1"):
            objs.append(obj)
            obj =  {}

        obj["SSID"] = kv[-1].strip()

    if ls[x].startswith("    Network type"):
        obj["Network"] = kv[-1].strip()
    


    if ls[x].startswith("    Authentication"):
        obj["Authentication"] = kv[-1].strip()
        obj["BSSIDS"] = {}
        
        

    if ls[x].startswith("    BSSID"):
        bssid = {}
        bssid["MAC"] = ":".join(kv[-6:]).strip()

    if ls[x].startswith("         Channel"):
        bssid["CH"] = kv[-1].strip()

    if ls[x].startswith("         Signal"):
        bssid["Signal"] = kv[-1].strip()

    if ls[x].startswith("         Radio Type"):
        bssid["CH"] = kv[-1].strip()

    if ls[x].startswith("         Basic rates"):
        bssid["BasicRates"] = kv[-1].strip()

    if ls[x].startswith("         Other rates"):
        bssid["OtherRates"] = kv[-1].strip()
        obj["BSSIDS"][bssid["MAC"]] = bssid

    x += 1
objs.append(obj)
pprint.pprint(objs)

for o in objs:
    if data.get(o.get("SSID", "Empty"), None):
        for k,v in o["BSSIDS"].items():
            if not k in data[o["SSID"]].get("BSSIDS", {}):
                data[o.get("SSID", "Empty")]["BSSIDS"][k] = v
                print("Added BSSID: %s to SSID: %s" % (k, o.get("SSID", "Empty")))

    else:
        data[o.get("SSID", "Empty")] = o
        print("Added SSID: %s" % o.get("SSID", "Empty"))
fh.seek(0)
fh.write(json.dumps(data))
