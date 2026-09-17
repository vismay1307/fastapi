from fastapi import FastAPI

app = FastAPI()

# express mai hum route ke baad handler likhte hai vese hi same hai fastapi main
# app.get("/", health_routr);
# function health_routr(req, res) {
#     res.json({
#         message: "This is a Health Route"
#     });
# }

@app.get("/")
def health_routr():
    return{
        "message":"This is a Health Route"
    }


