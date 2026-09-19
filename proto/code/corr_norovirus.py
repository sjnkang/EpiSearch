import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

df1 = pd.read_excel(r'C:\Research\WBE\data\search\Norovirus.xlsx')
df2 = pd.read_excel(r'C:\Research\WBE\data\sewage\0_removed\national_sewage_norovirus.xlsx')
df_merged = pd.merge(df1[['Week', 'Norovirus']], df2[['Week', 'Norovirus']], on='Week', suffixes=('_search', '_sewage'))

df_clean = df_merged[['Norovirus_search', 'Norovirus_sewage']].dropna()
n_points = len(df_clean)

r_value, p_value = pearsonr(df_clean['Norovirus_search'], df_clean['Norovirus_sewage'])

save_dir = r'C:\Research\WBE\result\corr\0_removed\Norovirus_2\search_2week_back'
os.makedirs(save_dir, exist_ok=True) 

plt.figure(figsize=(8, 6))
sns.regplot(
    x=df_clean['Norovirus_search'], 
    y=df_clean['Norovirus_sewage'],
    scatter_kws={'alpha': 0.6},
    line_kws={'color': 'red'}
)

plt.xlabel('Search Volume (Norovirus)')
plt.ylabel('Sewage Concentration (Norovirus) [copies/mL]')
plt.title(f'Correlation: Norovirus Search vs Sewage\n(R={r_value:.4f}, p={p_value:.2e})')
plt.tight_layout()

save_path = os.path.join(save_dir, '노로바이러스군+제반증상_corr.png')
plt.savefig(save_path, dpi=300)
plt.show()