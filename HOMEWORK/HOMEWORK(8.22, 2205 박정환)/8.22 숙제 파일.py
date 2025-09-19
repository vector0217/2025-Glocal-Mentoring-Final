import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

# 🔹 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')   # Windows: 맑은 고딕
# plt.rc('font', family='AppleGothic')   # macOS: 애플 고딕
# plt.rc('font', family='NanumGothic')   # Linux: 나눔고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

file_paths = [
    "heatwave_2021_07.csv",
    "heatwave_2022_07.csv",
    "heatwave_2023_07.csv",
    "heatwave_2024_07.csv",
    "heatwave_2025_07.csv"
]

# 연도별 통합 데이터프레임 생성
combined_df = pd.DataFrame()

for path in file_paths:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()  # 공백 제거
    if '일시' in df.columns:
        df['일시'] = pd.to_datetime(df['일시'], errors='coerce')
        df['연도'] = df['일시'].dt.year
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# 연도별 평균 최고기온 계산
if '최고기온(°C)' in combined_df.columns:
    grouped = combined_df.groupby('연도')['최고기온(°C)'].mean().reset_index()
else:
    print("⚠️ '최고기온(°C)' 열이 존재하지 않습니다.")

# 📊 연도별 평균 최고기온 시각화 (한글 버전)
plt.figure(figsize=(12, 6))
plt.plot(grouped['연도'], grouped['최고기온(°C)'], marker='o', color='tomato')
plt.title("연도별 7월 평균 최고기온", fontsize=15)
plt.xlabel("연도")
plt.ylabel("평균 최고기온 (°C)")
plt.xticks(range(2021, 2026))
plt.grid(True)
plt.tight_layout()
plt.show()
