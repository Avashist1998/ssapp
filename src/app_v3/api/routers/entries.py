from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from db.models import Entry, EntryBase, Message

router = APIRouter()


@router.get("/",
    response_model=List[Entry],
    responses={
        500: {"model": Message},
    },
)
async def get_entries(
    request: Request,
    event_id: Optional[str] = None,
    player_id: Optional[str] = None,
    offset: int = 1,
    limit: int = 10,
):
    """Entries endpoint"""
    try:
        entries: List[Entry] = request.app.db_service.get_entries(
            request.app.db, event_id, player_id, offset, limit
        )
        return entries
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=500, content={"message": "Something went wrong"}
        )


@router.get("/{entry_id}",
    response_model=Entry,
    responses={
        404: {"model": Message},
        500: {"model": Message},
    },
)
async def get_entry(request: Request, entry_id: str):
    """Entry endpoint"""
    try:
        entry: Entry = request.app.db_service.get_entry(request.app.db, entry_id)
        if entry is None:
            return JSONResponse(
                status_code=404,
                content={"message": f"Entry with {entry_id=} does not exist"},
            )
        return entry
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=500, content={"message": "Something went wrong"}
        )


@router.post(
    "/",
    response_model=Entry,
    responses={
        404: {"model": Message},
        500: {"model": Message},
        400: {"model": Message},
    },
)
async def create_entry(request: Request, entry: EntryBase):
    """Create entry endpoint"""
    try:
        event = request.app.db_service.get_event(request.app.db, entry.event_id)
        player = request.app.db_service.get_player(request.app.db, entry.player_email)
        if player is None:
            return JSONResponse(
                status_code=404,
                content={
                    "message": f"Player with {entry.player_email=} does not exist"
                },
            )
        if event is None:
            return JSONResponse(
                status_code=404,
                content={"message": f"Event with {entry.event_id=} does not exist"},
            )
        if event.locked:
            return JSONResponse(
                status_code=400,
                content={"message": f"Event with {entry.event_id=} is locked"},
            )
        if player.email in [entry.player_email for entry in event.entries]:
            return JSONResponse(
                status_code=400,
                content={
                    "message":
                        f"Entry with {entry.event_id=} and {entry.player_email=} already exists"
                },
            )
        if event.limit is not None and event.limit == len(event.entries):
            return JSONResponse(
                status_code=400,
                content={"message": f"Event with {entry.event_id=} is full"},
            )
        created_entry = request.app.db_service.add_entry(request.app.db, entry)
        return created_entry
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to create entry"},
        )


@router.delete("/{entry_id}")
async def delete_entry(request: Request, entry_id: str):
    """Delete entry endpoint"""
    try:
        entry: Entry = request.app.db_service.get_entry(request.app.db, entry_id)
        if entry is None:
            return JSONResponse(
                status_code=404,
                content={"message": f"Entry with {entry_id=} does not exist"},
            )
        request.app.db_service.delete_entry(request.app.db, entry_id)
        return {"message": "Event deleted"}
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=500, content={"message": "Failed to delete entry"}
        )
