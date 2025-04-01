from fastapi import FastAPI
from .routers import links, users
from .database import engine
from .models import Base

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(links.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "URL Shortener API"}