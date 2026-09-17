from fastapi import FastAPI
from fastapi import Request
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

@app.get("/orders",description="LIST ORDERS1")
def orders():
    """LIST ORDERS"""
    return {
        "orders":[
            {
                "id":1,
                "name":"Butter Chicken",
                "status":"Delivered"
            },
            {"id":2,
                            "name":"Butter Masala Dosa",
                            "status":"Preparing"},
            {"id":3,
                            "name":"Mutton Biryani",
                            "status":"ON WAY"}
        ]
    }

@app.get("/debug/request-info")
async def request_info(request:Request):
    """Inspect The Raw Request Object"""
    return{
        "method":request.method,
        "url":str(request.url),
        "headers":dict(request.headers),
        "path_params":request.path_params,
        "query_params":dict(request.query_params),
    }

@app.get("/orders/get-active",
    summary="Get Active Orders",
    description=(
        "Return All Orders That Are Being Prepared"
    ),
    tags=["orders"],
    response_description="List Of All Active Orders"
)
def getactive():
    return{
        "Status":"Testing Successfull"
    }