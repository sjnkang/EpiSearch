import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression

# 1. 폰트 및 마이너스 기호 설정 (한글 폰트 적용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 분석할 파일 목록 설정
datasets = [
    {'name': 'SARS-CoV-2', 'file': r'C:\Research\WBE\data\nolag\results\nolag_SARS-CoV-2.xlsx'},
]

# 3. 반복문을 통해 각 질병별로 모델링, 시각화 및 예측값 저장 진행
for data in datasets:
    print(f"[{data['name']}] 데이터 분석 및 모델링 시작...")
    
    # 데이터 불러오기
    df = pd.read_excel(data['file'])
    
    # 결측치가 있을 경우 선형회귀 모델에서 오류가 나므로 제거
    df = df.dropna()
    
    # x축 시계열(Week) 설정
    if 'Week' in df.columns:
        df['Week'] = pd.to_datetime(df['Week'])
        x_axis = df['Week']
        df_model = df.drop(columns=['Week'])
    else:
        x_axis = df.index
        df_model = df

    # 타겟 변수(하수 농도) 자동 탐색
    target_col = [col for col in df_model.columns if 'ww conc.' in col.lower()]
    if not target_col:
        target_col = df_model.columns[0]
    else:
        target_col = target_col[0]

    # 예측에 사용할 피처(상관관계가 높은 속성들)
    features = [col for col in df_model.columns if col != target_col]
    
    # 실제 하수 농도 (y값)
    y = df_model[target_col]
    
    # --- 엑셀로 내보낼 예측값 데이터프레임 초기화 ---
    df_predictions = pd.DataFrame()
    if 'Week' in df.columns:
        df_predictions['Week'] = x_axis
    df_predictions['Actual_ww_conc'] = y.values
    # --------------------------------------------------
    
    # 4. 서브플롯(격자) 형태의 그래프 설정
    cols = 3  # 한 줄에 표시할 그래프 개수
    rows = math.ceil(len(features) / cols)
    if rows == 0: rows = 1
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4))
    if rows * cols > 1:
        axes = axes.flatten()
    else:
        axes = [axes]
    
    # 5. 각 속성별 단순 선형 회귀 모델 훈련, 예측 및 그래프 작성
    for i, feature in enumerate(features):
        # 독립 변수 (X값)
        X = df_model[[feature]]
        
        # 선형 회귀 모델 생성 및 학습
        model = LinearRegression()
        model.fit(X, y)
        
        # 예측 수행 및 설명력 계산
        y_pred = model.predict(X)
        r_squared = model.score(X, y) 
        
        # --- 예측값을 데이터프레임에 새로운 열로 추가 ---
        df_predictions[f'Predicted_by_{feature}'] = y_pred
        # --------------------------------------------------
        
        # 시계열 그래프 그리기
        ax = axes[i]
        ax.plot(x_axis, y, label='Actual ww conc.', color='black', linewidth=2)
        ax.plot(x_axis, y_pred, label=f'Predicted by {feature}', color='red', linestyle='--')
        
        ax.set_title(f"Predictor: {feature}\n$R^2$ = {r_squared:.3f}", fontsize=11)
        ax.legend(fontsize=9)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(alpha=0.3)

    # 6. 남는 빈 그래프(서브플롯) 공간 지우기
    for j in range(len(features), len(axes)):
        fig.delaxes(axes[j])
        
    # 전체 그래프 제목 및 레이아웃 설정
    plt.suptitle(f"{data['name']} - Simple Linear Regression Predictions", fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # 7. 이미지 파일로 저장
    img_save_path = rf'C:\Research\WBE\data\nolag\nolag_{data["name"]}_LR_predictions.png'
    plt.savefig(img_save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    # 8. 취합된 예측값 데이터를 엑셀 파일로 저장
    excel_save_path = rf'C:\Research\WBE\data\nolag\nolag_{data["name"]}_LR_predictions.xlsx'
    df_predictions.to_excel(excel_save_path, index=False)
    
    print(f"[{data['name']}] 시계열 예측 그래프 저장 완료: {img_save_path}")
    print(f"[{data['name']}] 예측값 데이터 저장 완료: {excel_save_path}\n")