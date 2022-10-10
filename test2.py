import requests
import json
url = "http://ddragon.leagueoflegends.com/cdn/12.9.1/data/en_US/champion.json"
res = requests.get(url = url)
data = res.json()
champs = list(data["data"].keys())
