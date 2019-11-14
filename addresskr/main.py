import json
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from shapely.geometry import shape, Point

df = pd.read_csv('csv/KOREA-ADDR-WGS84.csv', dtype=str)

def get_CTPRVN(lat, long):
    datas = df[df.SIG_CD.isna()]
    for _, row in datas.iterrows():
        point = Point(long, lat)
        poly = shape(json.loads(row.geometry))

        if poly.contains(point):
            return row.iloc[:3].to_dict()

    return None

def get_SIG(lat, long, CTPRVN=None):
    datas = df[(df.SIG_CD.notnull())&(df.EMD_CD.isna())]
    for _, row in datas.iterrows():
        point = Point(long, lat)
        poly = shape(json.loads(row.geometry))

        if poly.contains(point):
            return row.iloc[3:6].to_dict()

    return None

def get_EMD(lat, long):
    datas = df[df.EMD_CD.notnull()]
    for _, row in datas.iterrows():
        point = Point(long, lat)
        poly = shape(json.loads(row.geometry))

        if poly.contains(point):
            return row.iloc[6:9].to_dict()

    return None

def get_address(lat, long):
    datas = df[df.EMD_CD.notnull()]
    for _, row in datas.iterrows():
        point = Point(long, lat)
        poly = shape(json.loads(row.geometry))

        if poly.contains(point):
            return row.iloc[:-1].to_dict()

    return None


if __name__ == '__main__':
    HOME_lat, HOME_long = 37.38194, 126.6723 # 연세대 송도캠
    print(get_CTPRVN(HOME_lat, HOME_long))  # 인천
    print(get_SIG(HOME_lat, HOME_long))  # 연수구
    print(get_EMD(HOME_lat, HOME_long))  # 송도동
    print(get_address(HOME_lat, HOME_long))  # 주소
    
    SR_lat, SR_long = 37.4665612, 127.0227825 # 삼성전자 R&D캠퍼스
    print(get_CTPRVN(SR_lat, SR_long)) # 서울특별시
    print(get_SIG(SR_lat, SR_long)) # 서초구
    print(get_EMD(SR_lat, SR_long)) # 우면동
    print(get_address(SR_lat, SR_long))  # 주소
