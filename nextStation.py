"https://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList?serviceKey=MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D&routeId=200000010"

import requests
from bs4 import BeautifulSoup
import xmltodict 
import json
import pandas as pd

encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="

url = "https://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList"
station_Id = ""


def asdf(route_id):
    # real_url = "https://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList?serviceKey=MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D&routeId=200000010"
    # response = requests.get(real_url)
    params = {"serviceKey": decoding, "routeId": route_id}
    response = requests.get(url, params=params)
    return response

def parse_asdf(xml_data):
    content = xml_data.content 
    bus_route_dic = xmltodict.parse(content)
    return bus_route_dic

def make_df(dic_obj):
    jsonString = json.dumps(dic_obj['response']['msgBody']['busRouteStationList'])
    json_object = json.loads(jsonString)
    df = pd.DataFrame(json_object)
    # 원하는 columns만 골라서 만듬
    df = df[['stationId','stationName']]
    return df 


def next_station(route_id):
    dict_asdf = parse_asdf(asdf(route_id))
    df = make_df(dict_asdf)
    
    a = pd.DataFrame()
    b = pd.DataFrame()
    c = pd.DataFrame()
    
    b['nextStation'] = df['stationName'][1:len(df)]
    c = pd.DataFrame({'nextStation' : ['종점']})
    b = pd.concat([b,c], ignore_index=True)
    a  = pd.concat([df, b], axis = 1, ignore_index=True)
    # 이유는 모르겠는데 coulmns이름이 0 1 2 로 바껴있어서 rename함 
    # make_df에서 뽑아올거 추가하면 여기도 손봐야됨
    a.columns = ['stationId', 'stationName', 'nextStation']  
    
    return a

def next_station_df(df_route_id, station_Id):
    bus_stations = []
      
    for i in range(0, len(df_route_id)):
        route_id = df_route_id.iloc[i]
        df = next_station(route_id)
        df = df[df['stationId'] == station_Id]
        bus_stations.append(df)
    
    return bus_stations



#%%
# 예시
route_id = "200000010"
a = next_station(route_id)

#%%
station_Id = "202000003"  # 이걸 바꾸면 바뀜 233000076
import busname as bn
import busArrivalInfo as ai

d = ai.get_routeId(station_Id)
d_1 = bn.get_bus_names(d)
d_2 = pd.DataFrame(d_1)
#%%
abfg = next_station_df(d, station_Id)