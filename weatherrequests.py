from itsdangerous import json
import requests,json

payload = {'lat':'48.383777','lon':'10.852489','appid': 'c6af0952da356913b1e688030949c44b','units':'metric'} 
r =requests.get("https://api.openweathermap.org/data/2.5/weather",params=payload)


dictdata = json.loads(r.text)

print(json.dumps(dictdata,indent=4,sort_keys=True))

print(type(json.dumps(dictdata['main'])))

#print(json.dumps(dictdata['main']['temp'],indent=4,sort_keys=True))
#print(json.dumps(dictdata['main'],indent=4,sort_keys=True))



#for key,value in dictdata['main'].items():
#    print(key,value)