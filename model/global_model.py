import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os
import matplotlib.dates as mdates

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

train_path = r'C:\Research\EpiSearch\model\Influenza\data\train\global_Influenza.xlsx'
test_path  = r'C:\Research\EpiSearch\model\Influenza\data\test\global_Influenza.xlsx'

train_df = pd.read_excel(train_path)
test_df  = pd.read_excel(test_path)

train_df['Week'] = pd.to_datetime(train_df['Week'])
train_df.set_index('Week', inplace=True)

test_df['Week'] = pd.to_datetime(test_df['Week'])
test_df.set_index('Week', inplace=True)

X_train = train_df[['오한']]
y_train = train_df['Influenza ww conc.']

X_test = test_df[['오한']]
y_test = test_df['Influenza ww conc.']

model = LinearRegression()
model.fit(X_train, y_train)

save_dir = r'C:\Research\EpiSearch\model\Influenza'
os.makedirs(save_dir, exist_ok=True)

model_filename = os.path.join(save_dir, 'global_Influenza.pkl')
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")

predictions = model.predict(X_test)

predictions = np.maximum(0, predictions)

r2 = r2_score(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"--- Model 1 (전체 반영 모델) 성능 ---")
print(f"R-squared: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

full_actual_y = pd.concat([y_train, y_test])

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(full_actual_y.index, full_actual_y.values, label='실제 하수 농도 (2024~2026)', color='black', linewidth=2)

ax.plot(y_test.index, predictions, label='모델 예측 하수 농도 (2026)', color='blue', linestyle='--', linewidth=2.5, marker='x')

ax.axvline(x=y_test.index[0], color='red', linestyle=':', linewidth=2)

ax.set_xlim(full_actual_y.index.min(), full_actual_y.index.max())

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.xticks(rotation=45, ha='right')
metrics_text = f"R² : {r2:.4f}\nRMSE : {rmse:.4f}"
props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', alpha=0.9)

ax.set_title('Influenza 하수 농도 예측 결과 (전체 상관분석 반영)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Wastewater concentration (mg/L)', fontsize=12)
ax.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3)
plt.tight_layout()

save_img_dir = r'C:\Research\EpiSearch\model\Influenza'
os.makedirs(save_img_dir, exist_ok=True)

save_img_path = os.path.join(save_img_dir, 'global_Influenza.png')
plt.savefig(save_img_path, dpi=300, bbox_inches='tight')
print(f"Img saved as {save_img_path}")

plt.show()