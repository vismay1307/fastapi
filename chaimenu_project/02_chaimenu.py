from fastapi import FastAPI

app=FastAPI(
    title="SSIT CHAI MENU",
    description="This Is The Menu For SSIT TEA WALLAH-GRAD-2026",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json"

)

@app.get("/")
def health_route():
    """HEALTH CHECK ROUTE"""
    return{
        "message":"This Is An Health Route"
    }

