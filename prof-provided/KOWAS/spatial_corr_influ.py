import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from libpysal.weights import W
from esda.moran import Moran

# 1. 지역 설정 (영문)
regions = [
    'Seoul', 'Busan', 'Daegu', 'Incheon', 'Gwangju',
    'Daejeon', 'Ulsan', 'Sejong', 'Gyeonggi', 'Gangwon',
    'Chungbuk', 'Chungnam', 'Jeonbuk', 'Jeonnam',
    'Gyeongbuk', 'Gyeongnam', 'Jeju'
]

# 인접 행렬 설정
adj_matrix = [
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0], [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# 2. PySAL 가중치 객체 생성
neighbors = {i: [j for j, val in enumerate(row) if val == 1] for i, row in enumerate(adj_matrix) if sum(row) > 0}
w = W(neighbors)
w.transform = 'R'

# 3. 데이터 로드
df = pd.read_csv('national_sewage_influenza_log_scale.csv')

results = []

# 4. 분석 루프
for index, row in df.iterrows():
    # 'Week' 값을 가져와서 float로 먼저 바꾼 뒤 int로 변환
    # 데이터에 '37.0' 혹은 '37'이 섞여 있어도 안전하게 처리됩니다.
    week_raw = row['Week']

    try:
        # 혹시 '주'가 포함되어 있을 경우를 대비해 처리 후 변환
        if isinstance(week_raw, str):
            week_val = float(week_raw.replace('주', ''))
        else:
            week_val = float(week_raw)

        week_int = int(week_val)
    except ValueError:
        print(f"Skipping row {index}: Invalid week value {week_raw}")
        continue

    # 이후 분석 로직 동일...
    try:
        concentration_data = pd.to_numeric(row[regions], errors='coerce').astype(float).values
    except Exception as e:
        print(f"Week {week_int} conversion error: {e}")
        continue

    # (이하 기존 코드와 동일)
    valid_indices = list(w.neighbors.keys())
    filtered_data = np.nan_to_num(concentration_data[valid_indices])
    mi = Moran(filtered_data, w)

    results.append({
        'Week': week_int,
        'Moran_I': float(mi.I),
        'P_value': float(mi.p_sim),
        'Z_score': float(mi.z_sim)
    })

# 5. 결과 데이터프레임 생성
results_df = pd.DataFrame(results)

# 데이터의 분포를 전반적으로 파악할 수 있습니다.
print(results_df[['Moran_I', 'P_value', 'Z_score']].describe())

avg_moran = results_df['Moran_I'].mean()
avg_p_value = results_df['P_value'].mean()
avg_z_score = results_df['Z_score'].mean()

print(f"Total Average Moran's I: {avg_moran:.4f}")
print(f"Total Average P-value: {avg_p_value:.4f}")
print(f"Total Average Z-value: {avg_z_score:.4f}")

# 데이터의 분포를 전반적으로 파악할 수 있습니다.
print(results_df[['Moran_I', 'P_value', 'Z_score']].describe())

# 5. 결과 출력 (소수점 4자리까지)
print("\n" + "="*50)
print(f"{'Week':<10} | {'Moran_I':<10} | {'P_value':<10} | {'Z_score':<10}")
print("-" * 50)

for index, row in results_df.iterrows():
    # 주차(Week)는 정수로, 나머지는 소수점 4자리 실수로 출력
    print(f"{int(row['Week']):<10} | {row['Moran_I']:<10.4f} | {row['P_value']:<10.4f} | {row['Z_score']:<10.4f}")
print("="*50)

# 6. 시각화
plt.figure(figsize=(14, 6))

# 선 그래프
sns.lineplot(data=results_df, x=range(len(results_df)), y='Moran_I', marker='o', color='b', linewidth=2, label="Moran's I")

# 기준선
plt.axhline(y=0, color='r', linestyle='--', linewidth=1, label="Random Distribution (0)")

# 유의미 구간 배경 (P < 0.05)
for i in range(len(results_df)):
    if results_df.loc[i, 'P_value'] < 0.05:
        plt.axvspan(i-0.5, i+0.5, color='gray', alpha=0.1)

# X축 설정 (제한 및 정수 라벨링)
plt.xlim(0, len(results_df) - 1)
plt.xticks(range(len(results_df)), results_df['Week'])

# Y축 점검 및 최적화
y_min = results_df['Moran_I'].min()
y_max = results_df['Moran_I'].max()
plt.ylim(y_min - 0.1, y_max + 0.1) # Y값이 잘리지 않도록 여유 공간 부여

#plt.title("Weekly Changes in Spatial Autocorrelation (Moran's I)", fontsize=16, pad=20)
plt.title("Influenza (Moran's I)", fontsize=16, pad=20)
plt.xlabel('Week (Number)', fontsize=12)
plt.ylabel("Moran's I Index", fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

# 피크 지점 주석
max_idx = results_df['Moran_I'].idxmax()
plt.annotate(f"Peak: {results_df.loc[max_idx, 'Moran_I']:.4f}",
             xy=(max_idx, results_df.loc[max_idx, 'Moran_I']),
             xytext=(max_idx, results_df.loc[max_idx, 'Moran_I'] + 0.05),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='center')

plt.tight_layout()
plt.show()