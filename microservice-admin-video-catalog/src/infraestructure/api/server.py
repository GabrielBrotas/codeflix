from fastapi import FastAPI
from .routes.category import categoryRouter

app = FastAPI()
app.include_router(categoryRouter)


@app.get("/")
async def root():
    return {"message": "Hello World"}
