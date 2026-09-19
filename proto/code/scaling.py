import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. 분석할 파일 목록 설정 (3개 질병 한 번에 처리)
datasets = [
    {'name': 'Influenza', 'file': r'C:\Research\WBE\data\stepwise_Influenza.xlsx'},
    {'name': 'Norovirus', 'file': r'C:\Research\WBE\data\stepwise_Norovirus.xlsx'}
]

# 스케일러 설정 (0~100 범위)
scaler = MinMaxScaler(feature_range=(0, 100))

# 2. 반복문을 통해 각각의 데이터를 스케일링하고 새로운 엑셀로 저장
for data in datasets:
    # 데이터 불러오기
    df = pd.read_excel(data['file'])
    
    # 스케일링을 위해 날짜(Week) 열 분리
    if 'Week' in df.columns:
        df_week = df['Week']
        df_numeric = df.drop(columns=['Week'])
    else:
        df_week = None
        df_numeric = df

    # MinMaxScaler를 사용하여 수치형 데이터 스케일링 (0~100)
    df_scaled_numeric = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)

    # 분리해두었던 'Week' 열을 스케일링된 데이터프레임 맨 앞에 다시 추가
    if df_week is not None:
        df_scaled = pd.concat([df_week, df_scaled_numeric], axis=1)
    else:
        df_scaled = df_scaled_numeric
        
    # 3. 스케일링된 데이터를 새로운 엑셀 파일로 저장
    save_path = rf'C:\Research\WBE\data\stepwise_{data["name"]}_scaled.xlsx'
    df_scaled.to_excel(save_path, index=False)
    
    # 진행 상황 출력
    print(f"[{data['name']}] 데이터 스케일링 완료 및 저장: {save_path}")

print("모든 파일의 스케일링 및 저장이 완료되었습니다.")