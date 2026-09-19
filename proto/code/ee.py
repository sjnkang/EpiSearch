import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 1. 데이터 로드 및 전처리
search_path = r'C:\Research\WBE\data\search\search_normalized.xlsx'
sewage_path = r'C:\Research\WBE\data\sewage\sewage_normalized.xlsx'

df_search = pd.read_excel(search_path)
df_sewage = pd.read_excel(sewage_path)

# 날짜 형식 변환 및 병합
df_search['Week'] = pd.to_datetime(df_search['Week'])
df_sewage['Week'] = pd.to_datetime(df_sewage['Week'])
df_merged = pd.merge(df_search, df_sewage, on='Week', how='inner')

# ---------------------------------------------------------
# 1. SARS-CoV-2 (코로나) 모델링
# 기준일: 2024-07-01
# ---------------------------------------------------------
df_covid = df_merged[df_merged['Week'] >= '2024-07-01'].dropna(subset=['SARS-CoV-2']).copy()

# 분석에 사용할 검색어 지정 (필요에 따라 가감하세요)
covid_features = ['코로나', '기침', '발열', '호흡곤란', '코로나제반증상']
X_covid = df_covid[covid_features]
y_covid = df_covid['SARS-CoV-2']

model_covid = LinearRegression()
model_covid.fit(X_covid, y_covid)
r2_covid = r2_score(y_covid, model_covid.predict(X_covid))

print("========== [1] SARS-CoV-2 (코로나) 모델 ==========")
print(f"분석 기간: {df_covid['Week'].min().date()} ~ {df_covid['Week'].max().date()}")
print(f"모델 설명력(R-squared): {r2_covid:.4f}")
for feature, coef in zip(covid_features, model_covid.coef_):
    print(f" - {feature} 회귀 계수: {coef:.4f}")
print("\n")


# ---------------------------------------------------------
# 2. Influenza (인플루엔자) 모델링
# 기준일: 2024-09-02
# ---------------------------------------------------------
df_flu = df_merged[df_merged['Week'] >= '2024-09-02'].dropna(subset=['Influenza']).copy()

flu_features = ['독감', '인플루엔자', '플루', '고열', '근육통', '오한']
X_flu = df_flu[flu_features]
y_flu = df_flu['Influenza']

model_flu = LinearRegression()
model_flu.fit(X_flu, y_flu)
r2_flu = r2_score(y_flu, model_flu.predict(X_flu))

print("========== [2] Influenza (독감) 모델 ==========")
print(f"분석 기간: {df_flu['Week'].min().date()} ~ {df_flu['Week'].max().date()}")
print(f"모델 설명력(R-squared): {r2_flu:.4f}")
for feature, coef in zip(flu_features, model_flu.coef_):
    print(f" - {feature} 회귀 계수: {coef:.4f}")
print("\n")


# ---------------------------------------------------------
# 3. Norovirus (노로바이러스) 모델링
# 기준일: 2024-09-02
# ---------------------------------------------------------
df_noro = df_merged[df_merged['Week'] >= '2024-09-02'].dropna(subset=['Norovirus']).copy()

noro_features = ['장염', '식중독', '구토', '물설사', '복통', '노로바이러스']
X_noro = df_noro[noro_features]
y_noro = df_noro['Norovirus']

model_noro = LinearRegression()
model_noro.fit(X_noro, y_noro)
r2_noro = r2_score(y_noro, model_noro.predict(X_noro))

print("========== [3] Norovirus (노로바이러스) 모델 ==========")
print(f"분석 기간: {df_noro['Week'].min().date()} ~ {df_noro['Week'].max().date()}")
print(f"모델 설명력(R-squared): {r2_noro:.4f}")
for feature, coef in zip(noro_features, model_noro.coef_):
    print(f" - {feature} 회귀 계수: {coef:.4f}")
print("\n")