import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# 1. 폰트 및 마이너스 기호 설정 (한글 폰트 적용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 분석할 파일 목록 설정 (3개 질병 한 번에 처리)
datasets = [
    {'name': 'SARS-CoV-2', 'file': r'C:\Research\WBE\search_3week_ahead\data\stepwise_SARS-CoV-2.xlsx'},
    {'name': 'Influenza', 'file': r'C:\Research\WBE\search_3week_ahead\data\stepwise_Influenza.xlsx'},
    {'name': 'Norovirus', 'file': r'C:\Research\WBE\search_3week_ahead\data\stepwise_Norovirus.xlsx'}
]

scaler = MinMaxScaler(feature_range=(0, 100))

# 3. 반복문을 통해 각각의 히트맵 생성 및 저장
for data in datasets:
    # 데이터 불러오기
    df = pd.read_excel(data['file'])
    
    # 상관분석에서 날짜(Week) 열은 제외
    if 'Week' in df.columns:
        df_corr = df.drop(columns=['Week'])
    else:
        df_corr = df

    # MinMaxScaler를 사용하여 데이터 스케일링
    df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=df_corr.columns)

    # Pearson 상관계수 계산
    corr_matrix = df_scaled.corr(method='pearson')
    
    # 그래프 설정
    plt.figure(figsize=(8, 6))
    
    # 히트맵 그리기
    # - annot=True: 상관계수 숫자 표시
    # - fmt='.2f': 소수점 둘째 자리까지 표시
    # - cmap='RdBu_r': -1(파란색) ~ 0(흰색) ~ 1(빨간색)로 이어지는 논문용 색상
    # - vmin=-1, vmax=1: 색상 기준을 -1에서 1로 고정
    sns.heatmap(corr_matrix, 
                annot=True, 
                cmap='RdBu_r', 
                vmin=-1, 
                vmax=1, 
                linewidths=0.5,           # 셀 사이 선 긋기 (가독성 향상)
                annot_kws={"size": 11},   # 숫자 크기
                cbar_kws={'label': 'Pearson Correlation Coefficient'})
    
    # 그래프 제목 설정
    plt.title(f"{data['name']} Correlation Heatmap", fontsize=14, fontweight='bold', pad=15)
    
    # x, y축 라벨 회전 (글자 겹침 방지)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    # 4. 고해상도(300 dpi) 이미지로 저장
    save_path = rf'C:\Research\WBE\search_3week_ahead\heatmaps\stepwise_{data["name"]}_heatmap.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # 출력
    plt.show()