from fastapi import FastAPI
from infraestructure.db import Base, engine
from .routes.category import categoryRouter

app = FastAPI()
app.include_router(categoryRouter)

# in a real app, the database schemas would be managed by Alembic
# this assumes all routes import the models so they are bound to Base by this time
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}
