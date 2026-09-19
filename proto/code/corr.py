import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

df1 = pd.read_excel(r'C:\Research\WBE\data\search\single\single_복통.xlsx')
df2 = pd.read_excel(r'C:\Research\WBE\data\sewage\0_removed\national_sewage_norovirus.xlsx')
df_merged = pd.merge(df1[['Week', '복통']], df2[['Week', 'Norovirus']], on='Week')
d_points = len(df_merged)

df_clean = df_merged[['복통', 'Norovirus']].dropna()
n_points = len(df_clean)

r_value, p_value = pearsonr(df_clean['복통'], df_clean['Norovirus'])
print(f"[Norovirus] 데이터 초기 개수(N): {d_points}개")
print(f"[Norovirus] 데이터 개수(N): {n_points}개")
print(f"R값: {r_value:.4f}, P값: {p_value:.4e}")

save_dir = r'C:\Research\WBE\result\corr\0_removed\single\norovirus\search_2week_back'
os.makedirs(save_dir, exist_ok=True) 

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

plt.figure(figsize=(8, 6))
sns.regplot(
    x=df_clean['복통'], 
    y=df_clean['Norovirus'],
    scatter_kws={'alpha': 0.6},
    line_kws={'color': 'red'}
)

plt.xlabel('Search Volume (복통)')
plt.ylabel('Sewage Concentration (Norovirus) [copies/mL]')
plt.title(f'Correlation: 복통 Search vs Sewage\n(R={r_value:.4f}, p={p_value:.2e})')
plt.tight_layout()

save_path = os.path.join(save_dir, 'national_복통_norovirus_corr.png')
plt.savefig(save_path, dpi=300)
plt.show()