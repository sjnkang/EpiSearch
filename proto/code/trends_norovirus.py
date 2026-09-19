import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. 폰트 및 마이너스 기호 설정 (한글 폰트 적용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기 (노로바이러스 파일 경로로 수정)
file_path = r'C:\Research\WBE\data\Norovirus.xlsx'
df = pd.read_excel(file_path)

# [중요] x축을 월별로 표기하기 위해 Week 열을 날짜(datetime) 형식으로 변환
df['Week'] = pd.to_datetime(df['Week'])

# 3. 논문용 색상 지정
color_wbe = "#FF0000"      # 하수 농도: 명확한 붉은색 (Brick Red)
color_noro = "#1F24B4"     # 노로바이러스: 파란색 (Muted Blue)
color_enteritis = "#FF9F0E"# 장염: 주황색 (Safety Orange)
color_poison = '#2CA02C'   # 식중독: 녹색 (Cooked Green)
color_vomit = '#9467BD'    # 구토: 보라색 (Muted Purple)
color_diarrhea = '#8C564B' # 물설사: 갈색 (Chestnut Brown)
color_stomach = '#E377C2'  # 복통: 분홍색 (Raspberry Yogurt)

# 4. 그래프 설정 및 그리기
fig, ax = plt.subplots(figsize=(7, 4)) # 논문에 적합한 가로세로 비율

# 메인 데이터 (하수 농도) - 실선, 굵게
ax.plot(df['Week'], df['Norovirus ww conc.'], label='Scaled Norovirus\nww conc.', 
        color=color_wbe, linewidth=2, linestyle='-.')

# 검색량 데이터 - 점선 및 다른 마커/선스타일 적용
ax.plot(df['Week'], df['노로바이러스'], label='Scaled "노로바이러스"\nsearch volume', 
        color=color_noro, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['장염'], label='Scaled "장염"\nsearch volume', 
        color=color_enteritis, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['식중독'], label='Scaled "식중독"\nsearch volume', 
        color=color_poison, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['구토'], label='Scaled "구토"\nsearch volume', 
        color=color_vomit, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['물설사'], label='Scaled "물설사"\nsearch volume', 
        color=color_diarrhea, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['복통'], label='Scaled "복통"\nsearch volume', 
        color=color_stomach, linewidth=1, linestyle='-')

# 5. X축 월별 표기 설정 (matplotlib.dates 활용)
ax.xaxis.set_major_locator(mdates.MonthLocator()) 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 

# 6. 논문용 그래프 디자인 (Spine 제거 및 축 정리)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 축 라벨 설정
ax.set_ylabel('Scaled Values (0~100)', fontsize=11, fontweight='bold', labelpad=10)

# x축 글씨 겹침 방지
plt.xticks(rotation=45)

# 그리드는 y축에만 연하게 적용
ax.grid(axis='y', linestyle='-', alpha=0.3)

# 범례 설정 (그래프 바깥쪽에 깔끔하게 배치)
ax.legend(frameon=False, loc='upper right', fontsize=6)

# 레이아웃 조정
plt.tight_layout()

# 7. 고해상도(300 dpi) 논문용 이미지로 저장 (파일명 노로바이러스로 변경)
plt.savefig(r'C:\Research\WBE\data\norovirus_trends.png', dpi=300, bbox_inches='tight')

# 출력
plt.show()