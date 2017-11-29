#!/usr/bin/python
import requests, getpass

url = "https://api.robinhood.com/api-token-auth/"
headers = { 
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "X-Robinhood-API-Version": "1.0.0",
    "Connection": "keep-alive",
    "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
} 
data = {
        "username" : "",
        "password" : ""
        }
r = requests.post(url, headers = headers, data = data)
mfa = getpass.getpass()
data['mfa_code'] = int(mfa)
s = requests.Session()
r = s.post(url, headers=headers,data=data)
print (r, r.json())
