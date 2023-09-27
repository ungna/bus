
# 버스노선 선택 -> routeName : 노선번호 리턴 

import pandas as pd
import requests 
from bs4 import BeautifulSoup


# bus_arrival_info
encoding = "MsMlVXwTa6iJaepslzIENgYMrdmGndKRzvqoMgWnBH2K2kUV0xJB/M+dHc1zFvKBSXkP2RoS9DQQqYUNrbjAQg=="
# RSET용 url
base_url = 'http://apis.data.go.kr/6410000/'
arrival_url = "busarrivalservice/getBusArrivalList"


def bus_arrival_info(station_id):
    url = base_url + arrival_url
    params = {'serviceKey': encoding, 'stationId': station_id}
    response = requests.get(url, params=params)
    return response.text


def parse_bus_arrival_info(response):
    xml_obj = BeautifulSoup(response, 'lxml-xml')
    rows = xml_obj.find_all('busArrivalList')
    if len(rows) == 0:
        print("도착 예정인 정보가 없습니다.")
    return rows


def make_df_bus_arrival(rows):
    rowList = []
    textList = []
    columnsList = []

    # 빈리스트에서 [0]을 못뽑아내서 도착정보가없으면 IndexError: list index out of range라는 오류가남
    column = rows[0].find_all()
    for i in range(0, len(column)):
        columnsList.append(column[i].name)

    for i in range(0, len(rows)):
        columns = rows[i].find_all()

        for j in range(0, len(columns)):
            eachColumn = columns[j].text
            textList.append(eachColumn)
        rowList.append(textList)
        textList = []

    df = pd.DataFrame(rowList, columns=columnsList)
    return df




def predict_arrival_time(station_Id):
    rows = parse_bus_arrival_info(bus_arrival_info(station_Id))
    df_bus_arrival = make_df_bus_arrival(rows)
    df_bus_arrival = df_bus_arrival[['predictTime1', 'predictTime2']]
    # 뒤에 오는 후속버스가 없으면 빈칸("")으로 표시되는데 이걸 x로 바꿈
    df_bus_arrival["predictTime2"].replace("", "x", inplace=True)
    return df_bus_arrival


def get_routeId(station_Id):
    rows = parse_bus_arrival_info(bus_arrival_info(station_Id))
    df_bus_arrival = make_df_bus_arrival(rows)
    df_bus_arrival = df_bus_arrival[['routeId']]
    return df_bus_arrival



#%%

station_Id = "200000093"

c = predict_arrival_time(station_Id)
d = get_routeId(station_Id)

