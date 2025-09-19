import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 환경 설정 (한글 폰트 등)
# =========================
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =========================
# 1) 데이터 로딩(안전하게)
# =========================
folder_path = r"C:\Users\User\Desktop\2025_glocal_mentoring\2025-glocal-mentoring-main (1)\2025-glocal-mentoring-main\HOMEWORK(8.22, 2205 박정환)"
file_list = sorted(glob.glob(os.path.join(folder_path, "heatwave_20*_07.csv")))  # heatwave_YYYY_07.csv

if not file_list:
    raise FileNotFoundError("해당 폴더에서 heatwave_20**_07.csv 파일을 찾지 못했습니다.")

def read_csv_smart(path):
    """utf-8-sig로 먼저 읽고, 핵심 키워드가 하나도 없으면 cp949로 재시도"""
    def looks_ok(df):
        cols = "".join(df.columns)
        return any(k in cols for k in ["일시","폭염","열대야","특보","자외선"])
    # try utf-8-sig
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        if looks_ok(df):
            return df
    except Exception:
        pass
    # fallback cp949
    return pd.read_csv(path, encoding="cp949", errors="ignore")

def find_col(columns, keyword):
    """열 이름에 특정 키워드가 포함된 첫 열 반환(없으면 None)"""
    for c in columns:
        if keyword in str(c):
            return c
    return None

all_df = []

for file in file_list:
    year = int(os.path.basename(file).split("_")[1])  # 파일명에서 연도 추출
    df = read_csv_smart(file)
    df.columns = df.columns.str.strip()

    # ---- O/X 열 표준화(대문자 O/X, 공백 제거)
    for key in ["폭염여부", "열대야", "폭염특보"]:
        col = find_col(df.columns, key)
        if col is not None:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.upper()
                .str.replace("0", "O")  # 0(제로) 오입력 방지
            )

    # ---- 자외선 지수 열 찾기
    # 우선 '자외선' 포함 열을 찾고, 그중 '단계'가 들어간 열을 우선 사용
    uv_cols = [c for c in df.columns if "자외선" in str(c)]
    uv_col = None
    if uv_cols:
        # '단계' 포함 우선
        stage_cols = [c for c in uv_cols if "단계" in str(c)]
        uv_col = stage_cols[0] if stage_cols else uv_cols[0]

    # ---- 자외선 단계 → 숫자 매핑(낮음=1, 보통=2, 높음=3, 매우높음=4, 위험=5)
    uv_map = {
        "낮음": 1, "보통": 2, "높음": 3,
        "매우높음": 4, "매우 높음": 4, "매우강함": 4, "매우 강함": 4,
        "위험": 5, "매우위험": 5, "매우 위험": 5
    }

    if uv_col is not None:
        uv_series = df[uv_col].astype(str).str.strip()
        # 숫자형 시도
        uv_num = pd.to_numeric(uv_series, errors="coerce")
        # 숫자 비율이 낮으면(대부분 문자인 경우) 단계 매핑으로 전환
        if uv_num.notna().sum() < max(1, int(0.6 * uv_series.notna().sum())):
            uv_series_norm = uv_series.str.replace(r"\s+", "", regex=True)
            uv_num = uv_series_norm.map(uv_map)
        df["자외선_값"] = uv_num
    else:
        df["자외선_값"] = pd.NA  # 자외선 열이 아예 없는 경우

    # ---- 연도 부여(파일명 기준)
    df["연도"] = year

    all_df.append(df)

data = pd.concat(all_df, ignore_index=True)

# 2021~2025만 사용
YEARS = list(range(2021, 2026))
data = data[data["연도"].isin(YEARS)]

# 분석에 필요한 실제 열 이름 다시 확보
col_heat = find_col(data.columns, "폭염여부")
col_night = find_col(data.columns, "열대야")
col_warn = find_col(data.columns, "폭염특보")

if col_heat is None or col_night is None or col_warn is None:
    missing = [("폭염여부", col_heat), ("열대야", col_night), ("폭염특보", col_warn)]
    missing = [k for k, v in missing if v is None]
    raise KeyError(f"필수 열 누락: {missing}. CSV의 열 이름을 확인하세요.")

# =========================
# 2) 지표 계산(연도별)
# =========================
# 폭염/열대야 일수(= 'O' 개수)
heatwave_days = (
    data[data[col_heat] == "O"].groupby("연도").size().reindex(YEARS, fill_value=0)
)
tropical_nights = (
    data[data[col_night] == "O"].groupby("연도").size().reindex(YEARS, fill_value=0)
)

# 폭염특보 비율
def ratio_O(s):
    n = s.notna().sum()
    return (s == "O").sum() / n if n > 0 else 0.0

heatwave_warning_ratio = (
    data.groupby("연도")[col_warn].apply(ratio_O).reindex(YEARS, fill_value=0.0)
)

# 자외선 평균(숫자화된 '자외선_값')
uv_mean = (
    data.groupby("연도")["자외선_값"].mean().reindex(YEARS)
)

# 만약 특정 연도에 자외선 데이터가 전혀 없어서 NaN이면 0으로 채워 그래프가 비지 않게 함
uv_mean_filled = uv_mean.fillna(0)

# =========================
# 3) 시각화(2x2 서브플롯)
# =========================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1) 폭염일수
axes[0, 0].bar(heatwave_days.index, heatwave_days.values, color="tomato")
axes[0, 0].set_title("연도별 폭염일수 (2021~2025)")
axes[0, 0].set_xlabel("연도"); axes[0, 0].set_ylabel("일수")
axes[0, 0].set_xticks(YEARS)

# 2) 열대야 발생일수
axes[0, 1].bar(tropical_nights.index, tropical_nights.values, color="orange")
axes[0, 1].set_title("연도별 열대야 발생일수 (2021~2025)")
axes[0, 1].set_xlabel("연도"); axes[0, 1].set_ylabel("일수")
axes[0, 1].set_xticks(YEARS)

# 3) 폭염특보 비율
axes[1, 0].plot(heatwave_warning_ratio.index, heatwave_warning_ratio.values,
                marker="o", linewidth=2)
axes[1, 0].set_title("연도별 폭염특보 비율 (2021~2025)")
axes[1, 0].set_xlabel("연도"); axes[1, 0].set_ylabel("비율")
axes[1, 0].set_xticks(YEARS)
axes[1, 0].set_ylim(0, 1)
axes[1, 0].grid(True, linestyle='--', alpha=0.5)

# 4) 자외선지수 평균(단계 값)
axes[1, 1].plot(uv_mean_filled.index, uv_mean_filled.values, marker="s", linewidth=2)
axes[1, 1].set_title("연도별 평균 자외선지수(단계) (2021~2025)")
axes[1, 1].set_xlabel("연도"); axes[1, 1].set_ylabel("평균 단계 (1~5)")
axes[1, 1].set_xticks(YEARS)
axes[1, 1].set_ylim(0, 5)
axes[1, 1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
