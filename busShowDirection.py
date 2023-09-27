"https://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList?serviceKey=MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D&routeId=200000010"

import requests
from bs4 import BeautifulSoup
import xmltodict 
import json
import pandas as pd

encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB%2FM%2BdHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg%3D%3D"
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="

url = "https://apis.data.go.kr/6410000/busrouteservice/getBusRouteStationList"


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
    df = df[['stationId','stationName','turnYn','stationSeq']]
    return df 


def bus_show_direction(route_id):
    # 데이터 파싱
    dict_asdf = parse_asdf(asdf(route_id))
    df = make_df(dict_asdf)
    
    # columns만들어서 각각(upper방향) (마지막은 회차지점이라고 넣기)  (lower방향) 넣음
    upper, lower = upper_lower(df)
    upper['방향'] = turning_point_station(df)
    upper.iloc[-1,4] = "회차지점"
    upper['stationName'] = upper['stationName'] + "  (" + upper['방향'] + ") 방향"
    
    lower['방향'] = end_point_station(df)
    lower.iloc[-1,4] = "종점"
    lower['stationName'] = lower['stationName'] + "  (" + lower['방향'] + ") 방향"

    # stationId stationName만 남기고 upper lower합침
    upper = upper[['stationName' , 'stationId']]
    lower = lower[['stationName', 'stationId']]
    result = pd.concat([upper, lower])
    
    return result

# 회차점
def turning_point_Seq(df):
    tunrning_station = df[df['turnYn'] == 'Y']['stationSeq']
    tunrning_station = tunrning_station.iloc[0]
    return tunrning_station

# 회차점 이름
def turning_point_station(df):
    tunrning_station = df[df['turnYn'] == 'Y']['stationName']
    tunrning_station = tunrning_station.iloc[0]
    return tunrning_station

# 종점
def end_point_station(df):
    end_station = df.iloc[-1]['stationName']
    return end_station


def upper_lower(df):
    upper = []
    lower = []
    
    stationSeq = turning_point_Seq(df)
    stationSeq = int(stationSeq)
    for i in range(0,stationSeq):
        t = []
        t = df.iloc[i]
        upper.append(t)
        
        
    for j in range(stationSeq, len(df)):
        t = []
        t = df.iloc[j]
        lower.append(t)
    
    # list를 daataframe으로 바꿈
    upper = pd.DataFrame(upper)
    lower = pd.DataFrame(lower)
    
    return upper, lower



#%%
# 예시
route_id = "200000010"

b = bus_show_direction(route_id)