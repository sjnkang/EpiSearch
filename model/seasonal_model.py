import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# 그래프 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

train_path = r'C:\Research\EpiSearch\model\Norovirus\data\train\seasonal_Norovirus.xlsx'
test_path  = r'C:\Research\EpiSearch\model\Norovirus\data\test\seasonal_Norovirus.xlsx'

train_df = pd.read_excel(train_path)
test_df  = pd.read_excel(test_path)

train_df['Week'] = pd.to_datetime(train_df['Week'])
train_df.set_index('Week', inplace=True)

test_df['Week'] = pd.to_datetime(test_df['Week'])
test_df.set_index('Week', inplace=True)

def create_seasonal_features(df):
    """데이터프레임에 계절 스위치를 곱하여 모델 입력 변수를 만드는 함수"""
    month = df.index.month
    
 
    spring_feature = df['노로바이러스s3'] * month.isin([3, 4, 5]).astype(int)
    
    autumn_feature = df['노로바이러스s1'] * month.isin([9, 10, 11]).astype(int)
    
    winter_feature = df['노로바이러스s3'] * month.isin([12, 1, 2]).astype(int)
    
    X = pd.DataFrame({
        'Spring_Feature': spring_feature,
        'Autumn_Feature': autumn_feature,
        'Winter_Feature': winter_feature
    }, index=df.index)
    
    return X

X_train = create_seasonal_features(train_df)
y_train = train_df['Norovirus ww conc.']

X_test = create_seasonal_features(test_df)
y_test = test_df['Norovirus ww conc.']

model = LinearRegression()
model.fit(X_train, y_train)

save_dir = r'C:\Research\EpiSearch\model\Norovirus'
os.makedirs(save_dir, exist_ok=True)

model_filename = os.path.join(save_dir, 'seasonal_Norovirus.pkl')
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")

predictions = model.predict(X_test)
predictions = np.maximum(0, predictions)

r2 = r2_score(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"R-squared: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

full_actual_y = pd.concat([y_train, y_test])

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(full_actual_y.index, full_actual_y.values, label='실제 하수 농도 (2024-2026)', color='black', linewidth=2)
ax.plot(y_test.index, predictions, label='모델 예측 하수 농도 (2026)', color='green', linestyle='--', linewidth=2.5, marker='x') # 계절 모델은 녹색 계열 사용
ax.axvline(x=y_test.index[0], color='red', linestyle=':', linewidth=2)

ax.set_xlim(full_actual_y.index.min(), full_actual_y.index.max())
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45, ha='right')

metrics_text = f"R² : {r2:.4f}\nRMSE : {rmse:.4f}"
props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', alpha=0.9)

ax.set_title('Norovirus 전체 기간 하수 농도 및 2026년 예측 결과', fontsize=15, fontweight='bold', pad=15)
ax.set_ylabel('Norovirus Wastewater concentration (mg/L)', fontsize=12)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)

plt.tight_layout()

save_img_path = os.path.join(save_dir, 'seasonal_Norovirus.png')
plt.savefig(save_img_path, dpi=300, bbox_inches='tight')
print(f"Img saved as {save_img_path}")

plt.show()