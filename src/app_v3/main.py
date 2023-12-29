from fastapi import FastAPI
from db import Base, engine, Session
from services.db_service.sqlite_service import SqliteService

from routers.events import router as events
from routers.players import router as players
from routers.entries import router as entries

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.db: Session = Session()
app.db_service: SqliteService = SqliteService()

app.include_router(events,tags=["events"], prefix="/events")
app.include_router(players,tags=["players"], prefix="/players")
app.include_router(entries,tags=["entries"], prefix="/entries")

@app.get("/")
async def root():
    return {"message": "Hello World"}
