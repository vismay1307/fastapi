from fastapi import FastAPI
from exception import (invalid_pincode_error_handler,InvalidPincodeError,pincode_not_found_handler,PincodeNotFoundError)
from models import (PinCodeRequest,LocationResponse,BulkReq,BulkResponse)
from data import pincode_db

app=FastAPI(
    title="Pincode LookUp",
    description="Helps automatic Fillup For Street And City Once You Enter Pincode",
    docs_url="/docs",
    redoc_url="/redocs",
)
app.add_exception_handler(PincodeNotFoundError,pincode_not_found_handler)
app.add_exception_handler(InvalidPincodeError,invalid_pincode_error_handler)

@app.get("/")
def health_check():
    return{
        "message":"Hey ! This Route Works Fine"
    }

@app.get("/pincode/{code}",response_model=LocationResponse)
def get_pincode(code:str):
    """GET STREET,CITY,STATE FROM PINCODE"""
    if len(code)!=6 or not code.isdigit():
        raise InvalidPincodeError(code, "Must Be Exactly 6 Digits")
    if code not in pincode_db:
        raise PincodeNotFoundError(code)
    return pincode_db[code]

@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkReq):

    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)

    return BulkResponse(
        status="Success",
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )