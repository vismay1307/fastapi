from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_routr():
    return{
        "message":"This is a Health Route"
    }