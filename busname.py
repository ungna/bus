
# 버스노선 선택 -> routeName : 노선번호 리턴 

import pandas as pd
import requests 
from bs4 import BeautifulSoup


# bus_name_info
decoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
# RSET용 url
base_url = 'http://apis.data.go.kr/6410000/'
route_url = "busrouteservice/getBusRouteInfoItem"



def bus_name_info(route_id):
    url = base_url + route_url
    params = {"serviceKey": decoding, "routeId": route_id}
    response = requests.get(url, params=params)
    return response.text


def parse_bus_name_info(response):
    xml_obj = BeautifulSoup(response, 'lxml-xml')
    rows = xml_obj.find('routeName')
    return rows.text


def get_bus_names(df_routeId):
    bus_names = []
    for i in range(0, len(df_routeId)):
        routeId = df_routeId.iloc[i]

    ########### 얘때문에 오래걸림S
    #### routeId를 한번에 조회가 안되고 하나씩 조회해야됨 다른 방법있나 찾아봤으나 못찾음
        busname_info = bus_name_info(routeId)
        bus_name = parse_bus_name_info(busname_info)
        bus_names.append(bus_name)
    return bus_names


def get_bus_name(route_id):
    busname_info = bus_name_info(route_id)
    bus_name = parse_bus_name_info(busname_info)
    return bus_name

#%%
route_id = "200000010"

a = get_bus_name(route_id)

#%%
a = parse_bus_name_info(bus_name_info(route_id))
