# api key is 97f5c958
import requests
import json
import boto3


movieDB = "http://www.omdbapi.com/?apikey=97f5c958&"

results = ""

for count in range(1, 100):
    response = requests.get(movieDB+"t="+str(count)+"&plot=full")
    results += json.dumps(response.json(), indent=2, sort_keys=True)
print(results)
