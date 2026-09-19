import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

df1 = pd.read_excel(r'C:\Research\WBE\search_2week_ahead\data\stepwise_Norovirus.xlsx')
df2 = pd.read_excel(r'C:\Research\WBE\search_2week_ahead\data\stepwise_Norovirus.xlsx')
df_merged = pd.merge(df1[['Week', '노로바이러스+구토']], df2[['Week', 'Norovirus ww conc.']], on='Week')
d_points = len(df_merged)

df_clean = df_merged[['노로바이러스+구토', 'Norovirus ww conc.']].dropna()
n_points = len(df_clean)

r_value, p_value = pearsonr(df_clean['노로바이러스+구토'], df_clean['Norovirus ww conc.'])
print(f"[Norovirus] 데이터 초기 개수(N): {d_points}개")
print(f"[Norovirus] 데이터 개수(N): {n_points}개")
print(f"R값: {r_value:.4f}, P값: {p_value:.4e}")

save_dir = r'C:\Research\WBE\search_2week_ahead\data'
os.makedirs(save_dir, exist_ok=True) 

plt.figure(figsize=(5, 4))
sns.regplot(
    x=df_clean['노로바이러스+구토'], 
    y=df_clean['Norovirus ww conc.'],
    scatter_kws={'alpha': 0.6},
    line_kws={'color': 'red'}
)

plt.xlabel('Search Volume for "노로바이러스+구토"')
plt.ylabel('Norovirus ww conc. [copies/mL]')
plt.title(f'Correlation: Norovirus Search vs Sewage\n(R={r_value:.4f}, p={p_value:.2e})')
plt.tight_layout()

save_path = os.path.join(save_dir, 'national_norovirus_corr.png')
plt.savefig(save_path, dpi=300)
plt.show()