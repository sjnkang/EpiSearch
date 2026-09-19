import pandas as pd

# 1. 파일 불러오기 (경로는 필요에 따라 수정하세요)
file_path = r"C:\Research\WBE\data\search\search.xlsx"
df = pd.read_excel(file_path)

# 2. 수치형 데이터만 선택 (Week 등 날짜/문자열 컬럼 제외)
numeric_cols = df.select_dtypes(include=['number']).columns

# 3. 0~100 Min-Max 정규화 수행
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    
    # 데이터가 모두 같은 값이라 분모가 0이 되는 것을 방지
    if max_val != min_val:  
        df[col] = (df[col] - min_val) / (max_val - min_val) * 100
    else:
        df[col] = 0

# 4. 결과를 새 엑셀 파일로 저장
output_path = r"C:\Research\WBE\data\search\normalized_search.xlsx"
df.to_excel(output_path, index=False)

print("정규화된 파일이 저장되었습니다:", output_path)