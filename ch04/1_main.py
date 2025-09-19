'''
실행 명령어
uvicorn 1_main:app --reload
'''
from fastapi import FastAPI
import uvicorn, nest_asyncio

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "안녕, API!"}

@app.post("/echo")
def echo(item: dict):
    return {"you_sent": item}

# 서버 실행 (백그라운드처럼 돌기 때문에 커널이 안 멈춤)
uvicorn.run(app, host="0.0.0.0", port=8000)