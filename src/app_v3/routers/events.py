from fastapi import APIRouter
from models import Event

router = APIRouter()

@router.get("/")
async def events(offset: int = 0, limit: int = 10):
    """Events endpoint"""
    if offset < 0:
        offset = 0
    if limit > 50:
        limit = 50
    if limit < 0:
        limit = 10

    return {"offset": offset, "limit": limit}


@router.get("/{event_id}")
async def get_event(event_id: str):
    """Event endpoint"""
    return {"event_id": event_id}


@router.post("/")
async def create_event(event: Event):
    """Create event endpoint"""
    print(event)
    return {"message": "Event created"}

@router.put("/{event_id}")
async def update_event(event_id: str, event: Event):
    """Update event endpoint"""
    print(event_id)
    print(event)
    return {"message": "Event updated"}

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    """Delete event endpoint"""
    print(event_id)
    return {"message": "Event deleted"}
