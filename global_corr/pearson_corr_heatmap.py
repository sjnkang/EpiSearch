import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

datasets = [
    
    {'name': 'Norovirus', 'file': r'C:\Research\EpiSearch\global_corr\sewage_1week_ahead\Norovirus.xlsx'},
    
]

scaler = MinMaxScaler(feature_range=(0, 100))

for data in datasets:
    df = pd.read_excel(data['file'])

    if 'Week' in df.columns:
        df_corr = df.drop(columns=['Week'])
    else:
        df_corr = df

    df_scaled = pd.DataFrame(scaler.fit_transform(df_corr), columns=df_corr.columns)

    corr_matrix = df_scaled.corr(method='pearson')
    
    plt.figure(figsize=(8, 6))
      
    sns.heatmap(corr_matrix, 
                annot=True, 
                cmap='RdBu_r', 
                vmin=-1, 
                vmax=1, 
                linewidths=0.5,
                annot_kws={"size": 11},
                cbar_kws={'label': 'Pearson Correlation Coefficient'})
    
    plt.title(f"{data['name']} Correlation Heatmap", fontsize=14, fontweight='bold', pad=15)
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    save_path = rf'C:\Research\EpiSearch\global_corr\sewage_1week_ahead\{data["name"]}_heatmap.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()