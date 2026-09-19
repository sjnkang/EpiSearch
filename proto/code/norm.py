import pandas as pd
from sklearn.preprocessing import MinMaxScaler

file_path = r'C:\Research\WBE\data\sewage\sewage.xlsx'
df = pd.read_excel(file_path)

df.set_index('Week', inplace=True)

numeric_cols = df.select_dtypes(include=['number']).columns

scaler = MinMaxScaler(feature_range=(0, 100))
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

save_path = r'C:\Research\WBE\data\sewage\sewage_normalized.xlsx'
df.to_excel(save_path)

print(f"'{save_path}'로 저장.")