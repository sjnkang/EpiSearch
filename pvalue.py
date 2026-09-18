import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import spearmanr

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

base_dir = r'C:\Research\EpiSearch\global_corr'

cases = [
    {'name': 'SARS-CoV-2', 'lag_folder': 'search_1week_ahead'},
    {'name': 'Influenza', 'lag_folder': 'search_2week_ahead'},
    {'name': 'Norovirus', 'lag_folder': 'search_2week_ahead'}
]

scaler = MinMaxScaler(feature_range=(0, 100))

for case in cases:
    file_path = os.path.join(base_dir, case['lag_folder'], f"{case['name']}.xlsx")
    
    if not os.path.exists(file_path):
        continue

    df = pd.read_excel(file_path)

    if 'Week' in df.columns:
        df_corr = df.drop(columns=['Week'])
    else:
        df_corr = df

    df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=df_corr.columns)

    p_matrix = pd.DataFrame(index=df_scaled.columns, columns=df_scaled.columns)
    
    for col1 in df_scaled.columns:
        for col2 in df_scaled.columns:
            corr, p_val = spearmanr(df_scaled[col1], df_scaled[col2])
            p_matrix.loc[col1, col2] = p_val
            
    p_matrix = p_matrix.astype(float)
    
    plt.figure(figsize=(14, 10))
      
    sns.heatmap(p_matrix, 
                annot=True, 
                fmt=".4f",
                cmap='Blues_r', 
                vmin=0, 
                vmax=1, 
                linewidths=0.5,
                annot_kws={"size": 11},
                cbar_kws={'label': 'P-value'})
    
    plt.title(f"{case['name']} ({case['lag_folder']}) P-value Heatmap", fontsize=14, fontweight='bold', pad=15)
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    save_dir = os.path.join(base_dir, case['lag_folder'])
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{case['name']}_pvalue_heatmap.png")
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()