import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

df1 = pd.read_excel(r'C:\Research\WBE\data\search\인플루엔자제반증상.xlsx')
df2 = pd.read_excel(r'C:\Research\WBE\data\sewage\0_removed\national_sewage_influenza.xlsx')
df_merged = pd.merge(df1[['Week', 'Influenza']], df2[['Week', 'Influenza']], on='Week', suffixes=('_search', '_sewage'))

df_clean = df_merged[['Influenza_search', 'Influenza_sewage']].dropna()
n_points = len(df_clean)

r_value, p_value = pearsonr(df_clean['Influenza_search'], df_clean['Influenza_sewage'])

save_dir = r'C:\Research\WBE\result\corr\0_removed\overall\Influenza_2\search_2week_back'
os.makedirs(save_dir, exist_ok=True) 

plt.figure(figsize=(8, 6))
sns.regplot(
    x=df_clean['Influenza_search'], 
    y=df_clean['Influenza_sewage'],
    scatter_kws={'alpha': 0.6},
    line_kws={'color': 'red'}
)

plt.xlabel('Search Volume (Influenza)')
plt.ylabel('Sewage Concentration (Influenza) [copies/mL]')
plt.title(f'Correlation: Influenza Search vs Sewage\n(R={r_value:.4f}, p={p_value:.2e})')
plt.tight_layout()

save_path = os.path.join(save_dir, '오한s_corr.png')
plt.savefig(save_path, dpi=300)
plt.show()