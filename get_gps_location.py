import requests, json
import pandas as pd




kako_key = "KakaoAK b958bdf89a2ea48dc1e8c2792f0483f7"
myAdd = "경기도 수원시 권선구 세권로108번길 10"
tempArr = []


def request_json(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    headers = {"Authorization": kako_key }
    api_json = json.loads(str(requests.get(url, headers=headers).text))
    return api_json


def getXY_from_json(addr):
    temparry = []
    res_json = request_json(addr)
    temparry.append(res_json['documents'][0]['x']) 
    temparry.append(res_json['documents'][0]['y']) 
    return temparry 
