import pandas as pd
from itertools import combinations

# 1. 파일 경로 설정 및 데이터 불러오기
file_path = r'C:\Research\WBE\data\s_Norovirus.xlsx'
df = pd.read_excel(file_path)

# 2. 조합을 만들 대상 검색어(컬럼) 목록 지정
target_columns = ['노로바이러스', '장염', '식중독', '구토', '물설사', '복통']

# 3. 결과를 담을 데이터프레임 생성 (원본 데이터 유지)
df_result = df.copy()

# 4. 6개부터 2개까지의 조합 생성 및 값 합산
# range(6, 1, -1)은 6, 5, 4, 3, 2 순서로 반복합니다.
for r in range(6, 1, -1):
    # 해당 개수(r)로 만들 수 있는 모든 컬럼 조합 생성
    for combo in combinations(target_columns, r):
        # 컬럼 이름 만들기 (예: '노로바이러스+장염+식중독')
        new_col_name = '+'.join(combo)
        
        # 선택된 조합의 컬럼 데이터만 뽑아서 가로(행) 방향으로 더하기
        df_result[new_col_name] = df[list(combo)].sum(axis=1)

# 5. 결과 확인 (총 생성된 컬럼 수 확인)
# 6개 조합(1) + 5개 조합(6) + 4개 조합(15) + 3개 조합(20) + 2개 조합(15) = 총 57개의 새로운 컬럼이 생성됩니다.
print(f"새롭게 생성된 컬럼 개수: {len(df_result.columns) - len(df.columns)}개")
print(df_result.head())

# 6. 처리된 데이터를 새로운 엑셀 파일로 저장
save_path = r'C:\Research\WBE\data\stepwise_Norovirus.xlsx'
df_result.to_excel(save_path, index=False)

print(f"\n데이터 처리가 완료되어 '{save_path}'에 저장되었습니다.")