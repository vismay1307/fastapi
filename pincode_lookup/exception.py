from fastapi.responses import JSONResponse
from fastapi import Request

class PincodeNotFoundError(Exception):
    def __init__(self, pincode:str):
        self.pincode=pincode

class InvalidPincodeError(Exception):
    def __init__(self,pincode:str,reason:str="Invalid Pincode Format"):
        self.pincode=pincode
        self.reason=reason

async def pincode_not_found_handler(req:Request,exc:PincodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error":"Pincode Not Found",
            "message":f"Pincode Not Found For This {exc.pincode}",
            "pincode":exc.pincode,
        }
    )

async def invalid_pincode_error_handler(req:Request,exc:InvalidPincodeError):
    return JSONResponse(
        status_code=400,
        content={
            "error":"Invalid Pincode",
            "message":f"Invalid Pincode For This {exc.pincode}",
            "pincode":exc.pincode,
            "reason":exc.reason,
        }
    )

       
