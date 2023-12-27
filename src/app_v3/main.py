from fastapi import FastAPI

from routers.events import router as events
from routers.players import router as players
from routers.entries import router as entries

app = FastAPI()
app.include_router(events,tags=["events"], prefix="/events")
app.include_router(players,tags=["players"], prefix="/players")
app.include_router(entries,tags=["entries"], prefix="/entries")

@app.get("/")
async def root():
    return {"message": "Hello World"}
