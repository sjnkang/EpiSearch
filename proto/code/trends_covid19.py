import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 1. 폰트 및 마이너스 기호 설정 (한글 폰트 적용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
file_path = r'C:\Research\WBE\data\SARS-CoV-2.xlsx'
df = pd.read_excel(file_path)

# [중요] x축을 월별로 표기하기 위해 Week 열을 날짜(datetime) 형식으로 변환
# (주의: 엑셀의 Week 데이터가 '2023-01-01' 같은 날짜 형태여야 정상 작동합니다)
df['Week'] = pd.to_datetime(df['Week'])

# 3. 논문용 색상 지정 (Tableau 10 팔레트 기반의 차분하고 구분이 명확한 색상)
color_wbe = "#FF0000"     # 하수 농도: 명확한 붉은색 (Brick Red)
color_corona = "#0051FF"  # 코로나: 차분한 파란색 (Muted Blue)
color_cough = "#FFA30E"   # 기침: 주황색 (Safety Orange)
color_fever = '#2CA02C'   # 발열: 녹색 (Cooked Green)
color_breath = '#9467BD'  # 호흡곤란: 보라색 (Muted Purple)

# 4. 그래프 설정 및 그리기
fig, ax = plt.subplots(figsize=(7, 4)) # 논문에 적합한 가로세로 비율

# 메인 데이터 (하수 농도) - 실선, 굵게
ax.plot(df['Week'], df['SARS-CoV-2 ww conc.'], label='Scaled SARS-CoV-2\nww conc.', 
        color=color_wbe, linewidth=2, linestyle='-.')

# 검색량 데이터 - 점선 및 다른 마커/선스타일 적용 (흑백 인쇄 시에도 구분되도록)
ax.plot(df['Week'], df['코로나'], label='Scaled "코로나"\nsearch volume', 
        color=color_corona, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['기침'], label='Scaled "기침"\nsearch volume', 
        color=color_cough, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['발열'], label='Scaled "발열"\nsearch volume', 
        color=color_fever, linewidth=1, linestyle='-')
ax.plot(df['Week'], df['호흡곤란'], label='Scaled "호흡곤란"\nsearch volume', 
        color=color_breath, linewidth=1, linestyle='-')

# 5. X축 월별 표기 설정 (matplotlib.dates 활용)
# 간격을 1개월 단위로 설정하고, '년-월' 형태로 출력
ax.xaxis.set_major_locator(mdates.MonthLocator()) 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 

# 6. 논문용 그래프 디자인 (Spine 제거 및 축 정리)
# 위쪽과 오른쪽 테두리 선을 없애서 깔끔하게 만듦
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 축 라벨 설정
ax.set_ylabel('Scaled Values (0~100)', fontsize=11, fontweight='bold', labelpad=10)

# x축 글씨 겹침 방지
plt.xticks(rotation=45)

# 그리드는 y축에만 연하게 적용 (데이터 흐름 방해 최소화)
ax.grid(axis='y', linestyle='-', alpha=0.3)

# 범례 설정 (그래프 안쪽 빈 공간 또는 바깥쪽에 깔끔하게 배치, 테두리 제거)
ax.legend(frameon=False, loc='upper right', fontsize=7)

# 레이아웃 조정
plt.tight_layout()

# 7. 고해상도(300 dpi) 논문용 이미지로 저장 (선택 사항)
plt.savefig(r'C:\Research\WBE\data\covid19_trends.png', dpi=300, bbox_inches='tight')

# 출력
plt.show()