from fastapi import FastAPI,Query,HTTPException
from chaimenu_data_ import menu_items
from chaimodel import MenuResponse,MenuItems
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

@app.get("/menu",response_model=MenuResponse)
def get_menu(category:str|None=Query(None,description="Filtered by Category")):
    """Menu Items Api"""
    if category:
        filtered=[item for item in menu_items if item["category"].lower()==category.lower()]
        if not filtered:
            raise HTTPException(status_code=404,detail=f"No Item Found in {category}")
        return MenuResponse(count=len(filtered),items=filtered)
    return MenuResponse(count=len(menu_items),items=menu_items)


@app.get("/menu/{item_id}",response_model=MenuItems)
def get_item(itemid:int):
    for item in menu_items:
        if item["id"]==itemid:
            return item
        raise HTTPException(status_code=404,detail=f"No Item Found in {itemid}")