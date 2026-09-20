import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

import joblib

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

train_path = r'C:\Research\EpiSearch\model\Influenza\data\train\seasonal_Influenza.xlsx'
test_path = r'C:\Research\EpiSearch\model\Influenza\data\test\seasonal_Influenza.xlsx'

train_df = pd.read_excel(train_path)
test_df = pd.read_excel(test_path)

train_df.replace('null', np.nan, inplace=True)
train_df.dropna(inplace=True)

test_df.replace('null', np.nan, inplace=True)
test_df.dropna(inplace=True)

train_df['Week'] = pd.to_datetime(train_df['Week'])
train_df.set_index('Week', inplace=True)

test_df['Week'] = pd.to_datetime(test_df['Week'])
test_df.set_index('Week', inplace=True)

def create_hybrid_features(df):

    month = df.index.month

    global_feature = df['오한s2']

    spring_feature = (
        df['인플루엔자n']
        * month.isin([3, 4, 5]).astype(int)
    )

    winter_feature = (
        df['인플루엔자s1']
        * month.isin([12, 1, 2]).astype(int)
    )

    X = pd.DataFrame({
        'Global_Influenza': global_feature,
        'Spring_Influenza': spring_feature,
        # 'Autumn_Influenza': autumn_feature,
        'Winter_Influenza': winter_feature
    }, index=df.index)

    return X

X_train = create_hybrid_features(train_df)
y_train = train_df['Influenza ww conc.']

X_test = create_hybrid_features(test_df)
y_test = test_df['Influenza ww conc.']

model = LinearRegression()

model.fit(X_train, y_train)

save_dir = r'C:\Research\EpiSearch\model\Influenza'

os.makedirs(save_dir, exist_ok=True)

model_filename = os.path.join(
    save_dir,
    'EpiSearch_linear_Influenza.pkl'
)

joblib.dump(model, model_filename)

print(f"Model saved as {model_filename}")

predictions = model.predict(X_test)

predictions = np.maximum(0, predictions)

r2 = r2_score(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print(f"R-squared (설명력): {r2:.4f}")
print(f"RMSE (평균 오차): {rmse:.4f}")

print("\n=== Regression Coefficients ===")

for feature, coefficient in zip(
    X_train.columns,
    model.coef_
):
    print(f"{feature}: {coefficient:.6f}")

print(f"Intercept: {model.intercept_:.6f}")

full_actual_y = pd.concat([y_train, y_test])

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    full_actual_y.index,
    full_actual_y.values,
    label='실제 하수 농도 (2024-2026)',
    color='black',
    linewidth=2
)

ax.plot(
    y_test.index,
    predictions,
    label='모델 예측 하수 농도 (2026)',
    color='red',
    linestyle='--',
    linewidth=2.5,
    marker='x'
)

ax.axvline(
    x=y_test.index[0],
    color='gray',
    linestyle=':',
    linewidth=2
)

ax.set_xlim(
    full_actual_y.index.min(),
    full_actual_y.index.max()
)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(
    mdates.DateFormatter('%Y-%m')
)

plt.xticks(
    rotation=45,
    ha='right'
)

ax.set_title(
    'Influenza 전체 기간 하수 농도 및 2026년 예측 결과',
    fontsize=15,
    fontweight='bold',
    pad=15
)

ax.set_ylabel(
    'Influenza Wastewater concentration (mg/L)',
    fontsize=12
)

ax.legend(
    fontsize=11,
    loc='upper right'
)

ax.grid(
    True,
    alpha=0.3
)


plt.tight_layout()

save_img_path = os.path.join(
    save_dir,
    'EpiSearch_linear_Influenza.png'
)

plt.savefig(
    save_img_path,
    dpi=300,
    bbox_inches='tight'
)

print(f"Img saved as {save_img_path}")

plt.show()