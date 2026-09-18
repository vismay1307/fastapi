from pydantic import BaseModel


class MenuItems(BaseModel):
    id:int
    name:str
    price:float
    description:str
    category:str
    available:bool


class MenuResponse(BaseModel):
    status:str="success"
    count:int
    items:list[MenuItems]