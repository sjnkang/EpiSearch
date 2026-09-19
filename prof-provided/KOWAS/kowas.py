import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. 데이터 불러오기
try:
    # Adding encoding parameter to handle non-UTF-8 file encodings
    df = pd.read_csv('national_sewage_noro_log_scale.csv', encoding='UTF-8')  # Replace 'ISO-8859-1' if required
except UnicodeDecodeError:
    print("파일 인코딩 문제가 발생했습니다. 파일의 인코딩을 확인하거나 다른 인코딩을 시도하세요.")
    exit()
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
    exit()

# 2. 데이터 전처리
# '주차' 컬럼은 문자열이므로 상관분석에서 제외합니다.
df_numeric = df.drop(columns=['주차'], errors='ignore')

# 3. 상관계수 산출 (Pearson correlation)
corr_matrix = df_numeric.corr()

# 4. 히트맵 시각화 설정
plt.figure(figsize=(15, 12))

# 한글 깨짐 방지 (Windows: Malgun Gothic, Mac: AppleGothic)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    cbar_kws={"shrink": 0.8}
)

plt.title('Regional Virus Concentration Correlation Heatmap', fontsize=20, pad=20)
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# 5. 이미지 저장
output_path = 'heatmap_output.png'  # Define the output file path
plt.tight_layout()

# Save the plot with high resolution
plt.savefig(output_path, dpi=300)
plt.show()

print(f"Heatmap saved as {output_path}")