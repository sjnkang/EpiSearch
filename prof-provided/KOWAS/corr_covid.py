import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. 데이터 로드
df = pd.read_csv('national_sewage_covid_log_scale.csv')

# '주차' 컬럼은 분석에서 제외 (지역별 상관관계만 확인)
df_numeric = df.drop(columns=['Week'])

# 2. 피어슨 상관계수 계산
corr_matrix = df_numeric.corr(method='pearson')

# 3. 히트맵 시각화 설정
# 한글 깨짐 방지를 위해 나눔고딕 등 한글 폰트 설정이 필요할 수 있습니다.
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 기준 (Mac은 AppleGothic)
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(14, 10))


# 히트맵 그리기
ax=sns.heatmap(corr_matrix,
            annot=True,           # 수치 표시
            fmt=".2f",            # 소수점 둘째 자리까지
            cmap='RdYlBu_r',      # 이미지와 유사한 Red-Yellow-Blue 컬러맵 (역순)
            linewidths=0.5,       # 셀 사이 간격
            # [수정] 셀 안의 숫자(annot) 크기 조절
            annot_kws={"size": 13, "weight": "bold"},
            # [수정] 컬러바(범례) 설정
            cbar_kws={"shrink": .8},
            vmin=0,
            vmax=1
            )

# [추가] 컬러바 레이블 폰트 크기 조절
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=15)

#plt.title('Regional Correlation of Nationwide Wastewater-Based Noro Virus Concentrations (Pearson Correlation)', fontsize=15)
# [수정] x축 지명 크기 및 회전
plt.xticks(rotation=45, fontsize=16)#, fontweight='bold')

# [수정] y축 지명 크기
plt.yticks(rotation=0, fontsize=16)#, fontweight='bold')
plt.tight_layout()

# 결과 저장 및 출력
plt.savefig('sewage_covid_heatmap.png', dpi=300)
plt.show()