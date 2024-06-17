import uvicorn
from fastapi import FastAPI

from app.database import engine, Base
from app.endpoints import admin, playlists, sounds

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(playlists.router, tags=["playlists"])
app.include_router(sounds.router, tags=["sounds"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
