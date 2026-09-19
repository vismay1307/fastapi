from pydantic import BaseModel,field_validator

class PinCodeRequest(BaseModel):
    pincode:str 

    @field_validator("pincode")
    @classmethod
    def validatePincode(cls,val):
        if len(val)!=6 or not val.isDigit():
            raise ValueError("Pincode Must Be Exactly 6 Digits")
        return val

class LocationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district:str

class BulkReq(BaseModel):
    pincodes:list[str]

    @field_validator("pincodes")
    @classmethod
    def validatePincodes(cls,val):
        if len(val)==0:
            raise ValueError("At Least One Pincode Is Req")
        if len(val)>20:
             raise ValueError("MAX 20")
        for code in val:
            if len(code)!=6 or not code.isdigit():
                        raise ValueError("Each Pincode Must Be Exactly 6 Digits")
        return val

class BulkResponse(BaseModel):
    status: str = "Success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]