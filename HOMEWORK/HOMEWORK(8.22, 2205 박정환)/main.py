from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "안녕, API!"}

@app.post("/echo")
def echo(item: dict):
    return {"you_sent": item}

