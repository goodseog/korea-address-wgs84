#%%
import os
import json

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#%%
precision = 'orig'

with open(os.path.join('GeoJSON', f'TL_SCCO_CTPRVN_{precision}.json'), 'rt') as f:
    CTRPVN = json.load(f)

with open(os.path.join('GeoJSON', f'TL_SCCO_SIG_{precision}.json'), 'rt') as f:
    SIG = json.load(f)

with open(os.path.join('GeoJSON', f'TL_SCCO_EMD_{precision}.json'), 'rt') as f:
    EMD = json.load(f)

#%%
print(CTRPVN['features'][0].keys())

# %%
import pandas as pd
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

#%%

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
        'geometry': elem['geometry'],
    }, ignore_index=True)


# print(len(EMD['features']))
# print(CTRPVN['features'][0])

#%%
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
        'geometry': elem['geometry'],
    }, ignore_index=True)

#%%
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
        'geometry': elem['geometry'],
    }, ignore_index=True)

# %%
df.loc[df.CTPRVN_CD.isna(), 'CTPRVN_CD'] = df.loc[df.CTPRVN_CD.isna(), 'SIG_CD']
df.loc[df.CTPRVN_CD.isna(), 'CTPRVN_CD'] = df.loc[df.CTPRVN_CD.isna(), 'EMD_CD']
df.CTPRVN_CD = df.CTPRVN_CD.astype(str).str[:2].astype(int)

# %%
df.loc[df.SIG_CD.isna(), 'SIG_CD'] = df.loc[df.SIG_CD.isna(), 'EMD_CD']
df.SIG_CD = df.SIG_CD.astype(str).str[:5].astype(int)

# %%
df.loc[df.SIG_CD.str.len > 5, :] = df.loc[df.SIG_CD > 100000, :] // 1000 

# %%
df.tail()

# %%
