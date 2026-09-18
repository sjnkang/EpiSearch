import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 검색량 데이터 불러오기
file_path = r'C:\Research\EpiSearch\original_data\search\SARS-CoV-2\SARS-CoV-2_search.xlsx'
df = pd.read_excel(file_path)
df['Week'] = pd.to_datetime(df['Week'])

# 2. 하수 농도 데이터 불러오기
sewage_path = r'C:\Research\EpiSearch\original_data\sewage\sewage_normalized.xlsx'
df_sewage = pd.read_excel(sewage_path)
df_sewage['Week'] = pd.to_datetime(df_sewage['Week'])

keywords = [col for col in df.columns if col != 'Week']
num_keywords = len(keywords)
colors = plt.cm.get_cmap('tab20', num_keywords)

fig, ax = plt.subplots(figsize=(10, 5))

# 3. 검색량 키워드 그래프 그리기
for i, keyword in enumerate(keywords):
    ax.plot(df['Week'], df[keyword], label=keyword, color=colors(i), linewidth=1.5, linestyle='-')

# 4. 하수 농도 그래프 그리기
ax.plot(df_sewage['Week'], df_sewage['SARS-CoV-2 ww conc.'], 
        label='SARS-CoV-2 ww conc.', color='red', linewidth=2, linestyle='--')

# X축 설정
ax.xaxis.set_major_locator(mdates.MonthLocator()) 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 

# ==========================================
# ★ 수정된 부분: X축 한계 설정 (빈 공간 제거)
# ==========================================
# SARS-CoV-2 하수 농도 값이 존재하는(NaN이 아닌) 날짜만 추출
valid_sewage = df_sewage.dropna(subset=['SARS-CoV-2 ww conc.'])

# 검색량 시작일과 유효한 하수농도 시작일 중 '더 늦은 날짜'를 시작점으로 설정
min_date = max(df['Week'].min(), valid_sewage['Week'].min())

# 끝나는 날짜는 두 데이터 중 더 늦은 날짜로 설정
max_date = max(df['Week'].max(), valid_sewage['Week'].max())

ax.set_xlim(min_date, max_date)
# ==========================================

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_ylabel('Search & Sewage Volume', fontsize=11, fontweight='bold', labelpad=10)

plt.xticks(rotation=45)

ax.grid(axis='y', linestyle='-', alpha=0.3)

ax.legend(frameon=False, loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=7)

plt.tight_layout()

plt.savefig(r'C:\Research\EpiSearch\original_data\search\SARS-CoV-2\search&sewage_trends.png', dpi=300, bbox_inches='tight')

plt.show()