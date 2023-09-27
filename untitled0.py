"""경기도 기준으로 내가 원하는 버스의 도착 정보얻기 

1.버스노선 검색 
2.내 주 반ㅕ 200미터내 정류소 조회 -> 선택 
3.버스 도착 정보 조회 서비스

stationId:정류장 아이디
stationName:정류장 이름
routeId:노선 아이디
routeName:노선 번호 

predictTime1:가장 빨리 오는 그 노선 번호의 버스
predictTime2:두번 째로 빨리 오는 그 노선 번호의 버스


Created on Fri Sep 22 20:03:40 2023

112 번 노선id = 200000049

@author: find bus mini project team (sam & junhee)
"""

import pandas as pd
import requests 
import xmltodict 
import json
import streamlit as st
from bs4 import BeautifulSoup
from PIL import Image

import get_gps_location as gl 

import nextStation as ns
# a = ns.next_station(route_id)
# ns.next_station_df(df_route_id, station_Id)

import busShowDirection as sd
# b = sd.bus_show_direction(route_id)

import busArrivalInfo as ai
# ai.predict_arrival_time(station_Id)
# ai.get_routeId(station_Id)

import busname as bn
# bn.get_bus_name(route_id)
# bn.get_bus_names(df_routeId)


myAdd = "경기도 수원시 권선구 세권로108번길 10"
coord_xy = []
kakao_key = "KakaoAK b958bdf89a2ea48dc1e8c2792f0483f7"
my_add = "경기도 수원시 "

# REST용 url 만들기 
service_url = "http://apis.data.go.kr/6410000/busstationservice"
service_name = "/getBusStationAroundList"
encoding_key = "%2BltohkyQC0eQUMVVaH5qwUi4FxaROssy0kpwzEdkqsFqedo%2FKlvT05Ap0svSUr2xQsOHd9%2FK2pXWpnH5N%2BmTcg%3D%3D" 
auth_key = "?serviceKey=" + encoding_key

route_id = "200000010"
station_Id = "200000093"


#%%
# find_station_around_me

def find_station_around_me(final_url):
    bus_info_xml = requests.get(final_url)
    bus_route_df = make_df(xtod(bus_info_xml))
    #print(bus_route_df[["stationName","mobileNo","stationId"]])
    #return make_station_list(bus_route_df["stationName"])
    return bus_route_df[["stationName","mobileNo","stationId","x","y"]]

def xtod(xml_data):
    #contents 분리 
    content = xml_data.content 
    #dictionary 볂환 
    bus_route_dic = xmltodict.parse(content)
    return bus_route_dic

def make_df(dic_obj):
    jsonString = json.dumps(dic_obj['response']['msgBody']['busStationAroundList'])
    json_object = json.loads(jsonString)
    df = pd.DataFrame(json_object)
    return df 

def make_station_list(df):
    is_Suwon_bus = df['regionName'] == '수원'
    station_names = df[is_Suwon_bus]['stationName']
    return station_names

def set_coordination(coord_xy):
    x = coord_xy[0]
    y = coord_xy[1]
    coordination = f"&x={x}&y={y}"
    return coordination


#%%
xy_arr = gl.getXY_from_json(myAdd)

serviceKey = set_coordination(xy_arr) 
final_url = service_url+service_name+auth_key+serviceKey
a = requests.get(final_url)



#%%


st.write("안녕하세요 즐거운 출근을위한 findbus앱 입니다.")
myAdd = st.text_input('주소를 넣어주세요', '경기도 수원시 ') # 장안구 정조로 940-1
st.write("당신이 입력한 주소는" , myAdd,"맞죠 ?")
    

# 주소를 대입하여 위도 경도 x,y 좌표 읽어와 서비스 URL 대입함 
xy_arr = gl.getXY_from_json(myAdd)

serviceKey = set_coordination(xy_arr) 
final_url = service_url+service_name+auth_key+serviceKey


stations_around_me = find_station_around_me(final_url)

# selectbox에 넣을 정보(stationName)을 리스트로 만들어서 대입함
stations_around_me['stationNameandId'] = stations_around_me['stationName'] + "(" + stations_around_me['stationId'] + ")"
stationNameandId_list = stations_around_me.stationNameandId.to_list()
stationId_list = stations_around_me.stationId.to_list()

option = st.selectbox(
    'How would you like to be contacted?',
    stationNameandId_list)

st.write('You selected:', option)

if st.button(option):
    # 클릭했을때 option의 stationId가 나오게
    index_no = stationNameandId_list.index(option)
    station_Id = stationId_list[index_no]
    
    # 버스정보 조회

    predict_time = ai.predict_arrival_time(station_Id)
    get_routeId = ai.get_routeId(station_Id)
    
    bus_names_list = bn.get_bus_names(get_routeId)
    bus_names_df = pd.DataFrame(bus_names_list)

    # get_routeId_list을 뽑아와서 현재 station_id랑 비교해서 nextstation만 남김
    bus_names_list = ns.next_station_df(get_routeId, station_Id)

    aaaa = pd.DataFrame()
    for i in bus_names_list:
        a = i
        aaaa = pd.concat([aaaa, a], ignore_index=True)
    
    aaaa = aaaa['nextStation']


    # df에 concat하기
    df = pd.concat([predict_time,bus_names_df, aaaa], ignore_index=True, axis = 1)
        
    # 뽑아온 결과 출력
    for i in range(0, len(df)):
        busnum = df.iloc[i, 2]
        arrivetime1 = df.iloc[i, 0]
        arrivetime2 = df.iloc[i, 1]
        nextStation = df.iloc[i,3]
        
        # print(f"곧 도착: {busnum}번 버스 약 {arrivetime1}분, {arrivetime2}분 전, 다음정거장: {nextStation}")
        st.write(f"곧 도착: {busnum}번 버스 약 {arrivetime1}분, {arrivetime2}분 전, 다음정거장: {nextStation}")
    
else:
    st.write("다시 입력 해주세요.")




# 광고 모형
adv_img = Image.open('advertise.png')

st.image(adv_img, caption="Google Ad 입니다. 광고를 사랑해주세요 ^^")

    
    