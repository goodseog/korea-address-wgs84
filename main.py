import json
import pandas as pd
from IPython.display import display
from shapely.geometry import shape, Point

df = pd.read_csv('csv/KOREA-ADDR-WGS84.csv', dtype=str)

def find_CTPRVN(lat, long):
    datas = df.dropna()
    display(datas)
    for idx, row in datas.iterrows():
        point = Point(long, lat)
        polygon = shape(json.loads(row.geometry))
        if polygon.contains(point):
            return row
        else:
            print(f'not in {row.CTPRVN_KOR_NM}')
    return None



if __name__ == '__main__':
    print(find_CTPRVN(37.3819478,126.672394))