import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# 그래프 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

train_path = r'C:\Research\EpiSearch\model\Norovirus\data\train\seasonal_Norovirus.xlsx'
test_path  = r'C:\Research\EpiSearch\model\Norovirus\data\test\seasonal_Norovirus.xlsx'

train_df = pd.read_excel(train_path)
test_df  = pd.read_excel(test_path)

train_df.replace('null', np.nan, inplace=True)
train_df.dropna(inplace=True)

test_df.replace('null', np.nan, inplace=True)
test_df.dropna(inplace=True)

train_df['Week'] = pd.to_datetime(train_df['Week'])
train_df.set_index('Week', inplace=True)

test_df['Week'] = pd.to_datetime(test_df['Week'])
test_df.set_index('Week', inplace=True)

def create_hybrid_features(df):
    """전체(Global) 변수와 계절(Seasonal) 스위치 변수를 모두 결합"""
    month = df.index.month
    
    global_feature = df['노로바이러스s2']
    
    spring_feature = df['노로바이러스s3'] * month.isin([3, 4, 5]).astype(int)
    autumn_feature = df['노로바이러스s1'] * month.isin([9, 10, 11]).astype(int)
    winter_feature = df['노로바이러스s3'] * month.isin([12, 1, 2]).astype(int)
    
    X = pd.DataFrame({
        'Global_Norovirus': global_feature,
        'Spring_Norovirus': spring_feature,
        'Autumn_Norovirus': autumn_feature,
        'Winter_Norovirus': winter_feature
    }, index=df.index)
    
    return X

X_train = create_hybrid_features(train_df)
y_train = train_df['Norovirus ww conc.']

X_test = create_hybrid_features(test_df)
y_test = test_df['Norovirus ww conc.']

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

model = LassoCV(cv=5, random_state=42)
model.fit(X_train_scaled, y_train)

save_dir = r'C:\Research\EpiSearch\model\Norovirus'
os.makedirs(save_dir, exist_ok=True)

joblib.dump(model, os.path.join(save_dir, 'EpiSearch_Norovirus.pkl'))
joblib.dump(scaler, os.path.join(save_dir, 'EpiSearch_Norovirus_scaler.pkl'))
print("✅ Model and scaler saved successfully.")

predictions = model.predict(X_test_scaled)
predictions = np.maximum(0, predictions)

r2 = r2_score(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"R-squared (설명력): {r2:.4f}")
print(f"RMSE (평균 오차): {rmse:.4f}")

full_actual_y = pd.concat([y_train, y_test])

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(full_actual_y.index, full_actual_y.values, label='실제 하수 농도 (2024-2026)', color='black', linewidth=2)

ax.plot(y_test.index, predictions, label='모델 예측 하수 농도 (2026)', color='red', linestyle='--', linewidth=2.5, marker='x') 
ax.axvline(x=y_test.index[0], color='gray', linestyle=':', linewidth=2)

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

save_img_path = os.path.join(save_dir, 'EpiSearch_Norovirus.png')
plt.savefig(save_img_path, dpi=300, bbox_inches='tight')
print(f"Img saved as {save_img_path}")

plt.show()