'''
실행 명령어
uvicorn 3_dataAnalisys:app --reload
'''

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import matplotlib.pyplot as plt
import io
import uvicorn, nest_asyncio

# ───────────────────────────────────────
# combined_df 데이터 프레임 생성
# ───────────────────────────────────────
import pandas as pd

file_paths = [
    "ch04/heatwave_2021_07.csv",
    "ch04/heatwave_2022_07.csv",
    "ch04/heatwave_2023_07.csv",
    "ch04/heatwave_2024_07.csv",
    "ch04/heatwave_2025_07.csv",
]

combined_df = pd.DataFrame()
for path in file_paths:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    if "일시" in df.columns:
        df["일시"] = pd.to_datetime(df["일시"], errors="coerce")
        df["연도"] = df["일시"].dt.year
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# 필수 컬럼 체크
REQ_COLS = {"일시", "연도", "최고기온(°C)"}
if not REQ_COLS.issubset(combined_df.columns):
    raise RuntimeError(f"다음 컬럼이 필요합니다: {REQ_COLS} / 현재: {set(combined_df.columns)}")

# ───────────────────────────────────────
# 1) FastAPI
# ───────────────────────────────────────
app = FastAPI(title="Mini Heatwave API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                # 모든 오리진 허용
    allow_origin_regex=".*",            # 'null'(file://) 오리진까지 광범위 허용
    allow_credentials=False,            # file://일 땐 credentials X 권장
    allow_methods=["*"],
    allow_headers=["*"],
)

def _subyear(year: int | None) -> pd.DataFrame:
    if year is None:
        return combined_df.copy()
    sub = combined_df[combined_df["연도"] == int(year)].copy()
    if sub.empty:
        raise HTTPException(status_code=404, detail=f"{year}년 데이터 없음")
    return sub

# ───────────────────────────────────────
# 2) 엔드포인트 4개
# ───────────────────────────────────────

# (A) 헬스체크 + 기본 요약
@app.get("/health")
def health():
    years = sorted(combined_df["연도"].dropna().unique().tolist())
    return {"rows": int(len(combined_df)), "years": years}

# (B) 연도별 요약(평균/최대/최소) + 폭염일수(기본 33도 이상)
@app.get("/summary")
def summary(
    year: int | None = Query(None, description="예: 2024"),
    threshold: float = Query(33.0, description="폭염 기준 °C (기본 33.0)")
):
    df = _subyear(year)
    heat_days = int((df["최고기온(°C)"] >= threshold).sum())
    out = {
        "year": year,
        "n_days": int(len(df)),
        "heatwave_days": heat_days,
        "threshold_C": threshold,
        "tmax_mean": float(df["최고기온(°C)"].mean()),
        "tmax_max": float(df["최고기온(°C)"].max()),
        "tmax_min": float(df["최고기온(°C)"].min()),
    }
    return JSONResponse(out)

# (C) 최고기온 상위 K일
@app.get("/top-heat-days")
def top_heat_days(
    year: int | None = Query(None),
    k: int = Query(5, ge=1, le=31, description="상위 일 수")
):
    df = _subyear(year)
    topk = df.sort_values("최고기온(°C)", ascending=False).head(k)
    return {
        "year": year,
        "k": k,
        "data": topk[["일시", "연도", "최고기온(°C)"]].to_dict(orient="records")
    }

# 서버 실행 (백그라운드처럼 돌기 때문에 커널이 안 멈춤)
uvicorn.run(app, host="0.0.0.0", port=8000)