import requests,json
import sys,os
from influxdb import InfluxDBClient

user = 'admin'
password = 'admin'
dbname = 'temperature'
query = 'select pressure from temperature;'
query_where = 'select temp from temperature where location=\'Stadtbergen\';'

payload = {'lat':'48.383777','lon':'10.852489','appid': 'c6af0952da356913b1e688030949c44b','units':'metric'} 

from datetime import datetime, timezone

def fetchAndPush(client):

    if(any(database['name'] == dbname for database in client.get_list_database() )):
        pass
    else:
        print("Create database: " + dbname)
        client.create_database(dbname)

    r =requests.get("https://api.openweathermap.org/data/2.5/weather",params=payload)

    dictdata =json.loads(r.text)

    json.dumps(dictdata['main'])

    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "location": dictdata['name'],
                "region": dictdata['sys']['country']
            },
            "time": dictdata['dt'] ,
            "fields": dictdata['main']
        }
    ]


    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    print("Querying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))


from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


if __name__ == "__main__":
    try:
        client = InfluxDBClient('52.91.50.199', '8087', user, password, dbname)
        rt = RepeatedTimer(10, fetchAndPush,client) # it auto-starts, no need of rt.start()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
