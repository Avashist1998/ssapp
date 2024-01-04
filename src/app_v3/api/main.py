from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, Session
from services.db_service.sqlite_service import SqliteService

from routers import events
from routers.players import router as players
from routers.entries import router as entries

app = FastAPI()

# origins = [
#     "http://localhost:5173",  # React app address
#     "http://localhost:3000",  # FastAPI server address
# ]
origins = [ "*" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.db: Session = Session()
app.db_service: SqliteService = SqliteService()

app.include_router(events.router, tags=["events"], prefix="/events")
app.include_router(players, tags=["players"], prefix="/players")
app.include_router(entries, tags=["entries"], prefix="/entries")

@app.get("/")
async def root():
    return {"message": "Hello World"}
