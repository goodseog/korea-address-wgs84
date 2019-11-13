# korea-address-wgs84
한국 WGS84 위도/경도 데이터를 빠르게 주소로 변환해주는 툴.
Tree 기반 서치로 속도 개선 목적
'서울특별시 서초구 우면동' 이면,

(lat, lon) -> isIn('서울특별시')
           -> isIn('서울특별시', '서초구')
           -> isIn('서울특별시', '서초구', '우면동')

으로 검색하여 속도 최적화

# Reference
http://www.gisdeveloper.co.kr/?p=2332