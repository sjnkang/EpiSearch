import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from libpysal.weights import W
from esda.moran import Moran_Local
from libpysal.weights.spatial_lag import lag_spatial

# 한글 폰트 설정 (Windows: 'Malgun Gothic', Mac: 'AppleGothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 및 가중치 설정 (이전과 동일)
regions = [
    'Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju',
    'Daejeon', 'Ulsan', 'Sejong', 'Gyeonggi', 'Gangwon',
    'Chungbuk', 'Chungnam', 'Jeonbuk', 'Jeonnam',
    'Gyeongbuk', 'Gyeongnam', 'Jeju'
]
#regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
adj_matrix = [
    [0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0], [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0], [0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0],
    [1,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0], [0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0],
    [0,0,0,0,0,1,0,1,1,1,0,1,1,0,1,0,0], [0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0], [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0],
    [0,0,1,0,0,0,1,0,0,1,1,0,1,0,0,1,0], [0,1,1,0,0,0,1,0,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

neighbors = {i: [j for j, val in enumerate(row) if val == 1] for i, row in enumerate(adj_matrix) if sum(row) > 0}
w = W(neighbors)
w.transform = 'R'

# 2. 파일 로드 및 43주차 데이터 추출
df = pd.read_csv('national_sewage_noro_log_scale.csv')

target_week = 7 #3,7,8,9 군집
'''
권고 시점
최소한으로 한다면 → Week 7

Moran's I 최고값(0.315), p = 0.029, Z = 2.133
군집이 가장 뚜렷한 시점이므로 LISA 결과가 가장 명확하게 나옴

충분히 분석한다면 → Week 3, 7, 8, 9 묶음

군집화가 시작되고(Week 3) 정점을 찍고(Week 7) 유지되는(Week 8–9) 흐름을 보여줄 수 있음
Discussion에서 "delayed clustering의 지속성"을 공간적으로 입증하는 근거가 됨

Week 4, 5는 선택적으로

p = 0.069, 0.082로 p < 0.10 수준
엄격한 기준(p < 0.05)으로는 제외하되, 탐색적 분석으로 포함할 수는 있음 — 단 논문에서 명시적으로 "exploratory"임을 밝혀야 함
'''


week_data = df[df['Week'] == target_week][regions].iloc[0]
valid_indices = list(w.neighbors.keys())
filtered_data = pd.to_numeric(week_data.iloc[valid_indices]).values

# 3. LISA 계산
lisa = Moran_Local(filtered_data, w)

# 4. 시각화 데이터 프레임 생성
lisa_res = pd.DataFrame({
    'Region': [regions[i] for i in valid_indices],
    'Concentration': filtered_data,
    'Quadrant': lisa.q,
    'P-value': lisa.p_sim
})

# 사분면 매핑 (1:HH, 2:LH, 3:LL, 4:HL)
quad_map = {1: 'HH (Hotspot)', 2: 'LH (Divergent)', 3: 'LL (Coldspot)', 4: 'HL (Divergent)'}
lisa_res['Type'] = lisa_res['Quadrant'].map(quad_map)
# 유의미하지 않은 데이터는 'Insignificant'로 분류
lisa_res.loc[lisa_res['P-value'] >= 0.05, 'Type'] = 'Insignificant'

# Moran Scatterplot
plt.figure(figsize=(10, 8))

z_data = (filtered_data - filtered_data.mean()) / filtered_data.std()
spatial_lag = lag_spatial(w, z_data)

sns.scatterplot(
    x=z_data,
    y=spatial_lag,
    hue=lisa_res['Type'],
    palette={
        'HH (Hotspot)': 'red',
        'LL (Coldspot)': 'blue',
        'LH (Divergent)': 'lightblue',
        'HL (Divergent)': 'orange',
        'Insignificant': 'lightgrey'
    },
    s=100
)

plt.axvline(0, color='black', linestyle='--')
plt.axhline(0, color='black', linestyle='--')

plt.title(f'Moran Scatterplot - Week {target_week} (Noro)', fontsize=15)
plt.xlabel('Virus concentration (Z-score)')
plt.ylabel('Spatial lag')

for i, txt in enumerate(lisa_res['Region']):
    plt.annotate(txt, (z_data[i], spatial_lag[i]),
                 xytext=(5, 5), textcoords='offset points')

plt.grid(alpha=0.3)
plt.show()