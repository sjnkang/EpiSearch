import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. 폰트 및 마이너스 기호 설정 (한글 폰트 적용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기 (인플루엔자 파일 경로로 수정)
file_path = r'C:\Research\WBE\data\Influenza.xlsx'
df = pd.read_excel(file_path)

# [중요] x축을 월별로 표기하기 위해 Week 열을 날짜(datetime) 형식으로 변환
df['Week'] = pd.to_datetime(df['Week'])

# 3. 논문용 색상 지정 (변수가 7개이므로 추가 색상 배정)
color_wbe = "#FF0000"      # 하수 농도: 명확한 붉은색 (Brick Red)
color_influ = "#0011FF"    # 인플루엔자: 파란색 (Muted Blue)
color_dokgam = "#FF9B0E"   # 독감: 주황색 (Safety Orange)
color_flu = '#2CA02C'      # 플루: 녹색 (Cooked Green)
color_fever = '#9467BD'    # 고열: 보라색 (Muted Purple)
color_muscle = '#8C564B'   # 근육통: 갈색 (Chestnut Brown)
color_chill = '#E377C2'    # 오한: 분홍색 (Raspberry Yogurt)

# 4. 그래프 설정 및 그리기
fig, ax = plt.subplots(figsize=(7, 4)) # 논문에 적합한 가로세로 비율

# 메인 데이터 (하수 농도) - 실선, 굵게
ax.plot(df['Week'], df['Influenza ww conc.'], label='Scaled Influenza\nww conc.', 
        color=color_wbe, linewidth=2, linestyle='-.')

# 검색량 데이터 - 점선 및 다른 마커/선스타일 적용 (흑백 인쇄 시 구분을 위해 패턴 교차)
ax.plot(df['Week'], df['인플루엔자'], label='Scaled "인플루엔자"\nsearch volume', 
        color=color_influ, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['독감'], label='Scaled "독감"\nsearch volume', 
        color=color_dokgam, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['플루'], label='Scaled "플루"\nsearch volume', 
        color=color_flu, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['고열'], label='Scaled "고열"\nsearch volume', 
        color=color_fever, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['근육통'], label='Scaled "근육통"\nsearch volume', 
        color=color_muscle, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['오한'], label='Scaled "오한"\nsearch volume', 
        color=color_chill, linewidth=1, linestyle='-')

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

# 7. 고해상도(300 dpi) 논문용 이미지로 저장 (파일명 변경)
plt.savefig(r'C:\Research\WBE\data\influenza_trends.png', dpi=300, bbox_inches='tight')

# 출력
plt.show()