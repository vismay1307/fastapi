from fastapi import FastAPI
from exception import (invalid_pincode_error_handler,InvalidPincodeError,pincode_not_found_handler,PincodeNotFoundError)
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

