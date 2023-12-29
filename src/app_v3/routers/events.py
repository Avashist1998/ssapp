from fastapi import APIRouter, Request, HTTPException


from models.event import Event, EventBase, EventCreate
from services.db_service import FailedToCreateException, FailedToGetException, FailedToDeleteException, FailedToUpdateException

router = APIRouter()

@router.get("/")
async def events(request: Request, offset: int = 1, limit: int = 10, creator_email: str = None, public: bool = True):
    """Events endpoint"""
    if offset < 1:
        offset = 1
    if limit > 50:
        limit = 50
    if limit < 0:
        limit = 10
    try:
        events = request.app.db_service.get_events(request.app.db, offset, limit, creator_email, public)
        if events is None:
            return HTTPException(status_code=404, detail="No events found")
        return {"events": events}
    except FailedToGetException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to get events")
    except Exception as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to get events")


@router.get("/{event_id}")
async def get_event(request: Request, event_id: int):
    """Event endpoint"""
    try:
        event = request.app.db_service.get_event(request.app.db, event_id)
        if event is None:
            return HTTPException(status_code=404, detail=f"Event with {event_id=} does not exist")
    except FailedToGetException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to get event")
    except Exception as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to get event")
    return {"event_id": event_id}


@router.post("/")
async def create_event(request: Request, event: EventBase):
    """Create event endpoint"""
    try:
        creator = request.app.db_service.get_player(request.app.db, event.creator)
        if creator is None:
            return HTTPException(status_code=404, detail=f"Player with {event.creator=} does not exist")
        res = request.app.db_service.add_event(request.app.db, event)
        if res is None:
            return HTTPException(status_code=500, detail="Failed to create event")
        return res
    except FailedToCreateException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to create event")
    except Exception as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to create event")

@router.put("/")
async def update_event(request: Request, event: EventBase):
    """Update event endpoint"""
    try:
        res = request.app.db_service.update_event(request.app.db, event)
        if res is None:
            return HTTPException(status_code=404, detail="Event does not exist")
        return res
    except FailedToUpdateException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to update event")
    except Exception as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to update event")

@router.delete("/{event_id}")
async def delete_event(request: Request, event_id: str):
    """Delete event endpoint"""
    try:
        request.app.db_service.delete_event(request.app.db, event_id)
        return {"message": "Event deleted"}
    except FailedToDeleteException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to delete event")
    except Exception as _:
        return HTTPException(status_code=500, detail="Failed to delete event")
