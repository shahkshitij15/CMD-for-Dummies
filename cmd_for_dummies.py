import requests
import os

if __name__ == '__main__':
    prevslotk = None
    prevslotv = None
    previp = ""
    while True:
        url = "http://0.0.0.0:5000/engtocmd"
        ip = input(">> ")
        if prevslotk is not None:
            prevslotv = ip
            res = requests.post(url, json={"eng": previp, "slots": {prevslotk: prevslotv}})
        else:
            res = requests.post(url, json={"eng": ip})
        res = res.json()
        if "res" in res:
            print(res["res"])
            prevslotk = res["slot"]
            previp = ip
        elif "cmd" in res:
            prevslotk = None
            prevslotv = None
            if len(res["cmd"]) == 1 and "cd" in res["cmd"][0]:
                os.chdir(res["cmd"][0][3:])
                continue
            q = ""
            for cmd in res["cmd"]:
                q = q + cmd + " \n "
            print(os.system(q))
