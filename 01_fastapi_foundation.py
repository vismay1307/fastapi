from fastapi import FastAPI

app = FastAPI(
    title="Swiggy Orders",
    description="API For Managing Orders",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json",
)


@app.get("/")
def read_route():
    """HEALTH CHECK"""
    return {
        "message": "This Is A Check Route",
        "status": "SUCCESS"
    }


@app.get("/about")
def about():
    """Return API METADATA"""
    return {
        "service": "Backend Team",
        "region": "Ahmedabad",
        "version": "1.1.1"
    }