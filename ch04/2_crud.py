'''
실행 명령어
uvicorn 2_crud:app --reload
'''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, nest_asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                # 모든 오리진 허용
    allow_origin_regex=".*",            # 'null'(file://) 오리진까지 광범위 허용
    allow_credentials=False,            # file://일 땐 credentials X 권장
    allow_methods=["*"],
    allow_headers=["*"],
)
# 임시 저장소 (실습용)
items = {
    1: {"name": "사과", "price": 1000},
    2: {"name": "바나나", "price": 2000}
}

# GET: 전체 아이템 목록
@app.get("/items")
def get_items():
    return items

# GET: 특정 아이템 조회
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템 없음")
    return items[item_id]

# POST: 새로운 아이템 추가
@app.post("/items/{item_id}")
def create_item(item_id: int, item: dict):
    if item_id in items:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이템")
    items[item_id] = item
    return {"msg": "추가 완료", "item": items[item_id]}

# PUT: 아이템 전체 수정
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템 없음")
    items[item_id] = item
    return {"msg": "수정 완료", "item": items[item_id]}

# DELETE: 아이템 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템 없음")
    del items[item_id]
    return {"msg": "삭제 완료"}

# 서버 실행 (백그라운드처럼 돌기 때문에 커널이 안 멈춤)
uvicorn.run(app, host="0.0.0.0", port=8000)