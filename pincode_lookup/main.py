from fastapi import FastAPI

app=FastAPI(
    title="Pincode LookUp",
    description="Helps automatic Fillup For Street And City Once You Enter Pincode",
    docs_url="/docs",
    redoc_url="/redocs",
)

@app.get("/")
def health_check():
    return{
        "message":"Hey ! This Route Works Fine"
    }

