import os
import json
import pandas as pd

print('load TL_SCCO_CTPRVN.json...')
f = open(os.path.join('GeoJSON', 'TL_SCCO_CTPRVN.json'), 'rt')
CTRPVN = json.load(f)
f.close()

print('load TL_SCCO_SIG.json...')
f = open(os.path.join('GeoJSON', 'TL_SCCO_SIG.json'), 'rt')
SIG = json.load(f)
f.close()

print('load TL_SCCO_EMD.json...')
f = open(os.path.join('GeoJSON', 'TL_SCCO_EMD.json'), 'rt')
EMD = json.load(f)
f.close()

datas = {
    'CTPRVN_CD': [],
    'CTPRVN_ENG_NM': [],
    'CTPRVN_KOR_NM': [],
    'SIG_CD': [],
    'SIG_ENG_NM': [],
    'SIG_KOR_NM': [],
    'EMD_CD': [],
    'EMD_ENG_NM': [],
    'EMD_KOR_NM': [],
    'geometry': [],
}

df = pd.DataFrame(datas)

print('merge CTPRVN info...')
for elem in CTRPVN['features']:
    df = df.append({
        'CTPRVN_CD': elem['properties']['CTPRVN_CD'],
        'CTPRVN_ENG_NM': elem['properties']['CTP_ENG_NM'],
        'CTPRVN_KOR_NM': elem['properties']['CTP_KOR_NM'],
        'SIG_CD': None,
        'SIG_ENG_NM': None,
        'SIG_KOR_NM': None,
        'EMD_CD': None,
        'EMD_ENG_NM': None,
        'EMD_KOR_NM': None,
        'geometry': json.dumps(elem['geometry']),
    }, ignore_index=True)


print('merge SIG info...')
for elem in SIG['features']:
    df = df.append({
        'CTPRVN_CD': None,
        'CTPRVN_ENG_NM': None,
        'CTPRVN_KOR_NM': None,
        'SIG_CD': elem['properties']['SIG_CD'],
        'SIG_ENG_NM': elem['properties']['SIG_ENG_NM'],
        'SIG_KOR_NM': elem['properties']['SIG_KOR_NM'],
        'EMD_CD': None,
        'EMD_ENG_NM': None,
        'EMD_KOR_NM': None,
        'geometry': json.dumps(elem['geometry']),
    }, ignore_index=True)

print('merge EMD info...')
for elem in EMD['features']:
    df = df.append({
        'CTPRVN_CD': None,
        'CTPRVN_ENG_NM': None,
        'CTPRVN_KOR_NM': None,
        'SIG_CD': None,
        'SIG_ENG_NM': None,
        'SIG_KOR_NM': None,
        'EMD_CD': elem['properties']['EMD_CD'],
        'EMD_ENG_NM': elem['properties']['EMD_ENG_NM'],
        'EMD_KOR_NM': elem['properties']['EMD_KOR_NM'],
        'geometry': json.dumps(elem['geometry']),
    }, ignore_index=True)

print('fill CTRPVN, SIG info...')
df.loc[df.SIG_CD.notnull(), 'CTPRVN_CD'] = df[df.SIG_CD.notnull()].SIG_CD.str[:2]
df.loc[df.EMD_CD.notnull(), 'CTPRVN_CD'] = df[df.EMD_CD.notnull()].EMD_CD.str[:2]
df.loc[df.EMD_CD.notnull(), 'SIG_CD'] = df[df.EMD_CD.notnull()].EMD_CD.str[:5]

for CTPRVN_CD in df.CTPRVN_CD.unique():
    df.loc[df.CTPRVN_CD == CTPRVN_CD, 'CTPRVN_ENG_NM'] = df.loc[df.CTPRVN_CD == CTPRVN_CD, 'CTPRVN_ENG_NM'].iloc[0]
    df.loc[df.CTPRVN_CD == CTPRVN_CD, 'CTPRVN_KOR_NM'] = df.loc[df.CTPRVN_CD == CTPRVN_CD, 'CTPRVN_KOR_NM'].iloc[0]

for SIG_CD in df.SIG_CD.dropna().unique():
    df.loc[df.SIG_CD == SIG_CD, 'SIG_ENG_NM'] = df.loc[df.SIG_CD == SIG_CD, 'SIG_ENG_NM'].iloc[0]
    df.loc[df.SIG_CD == SIG_CD, 'SIG_KOR_NM'] = df.loc[df.SIG_CD == SIG_CD, 'SIG_KOR_NM'].iloc[0]

df.to_csv('csv/KOREA-ADDR-WGS84.csv', index=False)
