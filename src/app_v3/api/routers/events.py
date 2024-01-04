from typing import Optional, Tuple, List
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from db.models import Event, EventBase, Message, EventsResponse
from services.db_service import (
    FailedToCreateException,
    FailedToGetException,
    FailedToDeleteException,
    FailedToUpdateException,
)

router = APIRouter()


@router.get("/", response_model=EventsResponse, responses={500: {"model": Message}})
async def get_events(
    request: Request,
    offset: int = 1,
    limit: int = 10,
    creator_email: str = None,
    public: Optional[bool] = None,
):
    """Events endpoint"""
    if offset < 1:
        offset = 1
    if limit > 50:
        limit = 50
    if limit < 0:
        limit = 10
    try:
        res: Optional[Tuple[int, List[Event]]] = request.app.db_service.get_events(
            request.app.db, offset, limit, creator_email, public
        )
        if res is None:
            return JSONResponse(status_code=404, content={"message": "No events found"})
        return EventsResponse(count=res[0], events=res[1])
    except FailedToGetException as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to get events"})
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to get events"})


@router.get("/{event_id}")
async def get_event(request: Request, event_id: int):
    """Event endpoint"""
    try:
        event = request.app.db_service.get_event(request.app.db, event_id)
        if event is None:
            return JSONResponse(
                status_code=404, content={"message": f"Event with {event_id=} does not exist"}
            )
        return event
    except FailedToGetException as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to get event"})
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to get event"})


@router.post("/")
async def create_event(request: Request, event: EventBase):
    """Create event endpoint"""
    try:
        creator = request.app.db_service.get_player(request.app.db, event.creator)
        if creator is None:
            return JSONResponse(
                status_code=404, content={"message": f"Player with {event.creator=} does not exist"}
            )
        res = request.app.db_service.add_event(request.app.db, event)
        if res is None:
            return JSONResponse(status_code=500, content={"message": "Failed to create event"})
        return res
    except FailedToCreateException as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to create event"})
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to create event"})


@router.put("/")
async def update_event(request: Request, event: EventBase):
    """Update event endpoint"""
    try:
        old_event = request.app.db_service.get_event(request.app.db, event.id)
        if old_event is None:
            return JSONResponse(
                status_code=404, content={"message": f"Event with {event.id=} does not exist"}
            )
        res = request.app.db_service.update_event(request.app.db, event)
        return res
    except FailedToUpdateException as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to update event"})
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to update event"})


@router.delete("/{event_id}")
async def delete_event(request: Request, event_id: str):
    """Delete event endpoint"""
    try:
        event = request.app.db_service.get_event(request.app.db, event_id)
        if event is None:
            return JSONResponse(
                status_code=404, content={"message": f"Event with {event_id=} does not exist"}
            )
        request.app.db_service.delete_event(request.app.db, event_id)
        return {"message": "Event deleted"}
    except FailedToDeleteException as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to delete event"})
    except Exception as _:
        return JSONResponse(status_code=500, content={"message": "Failed to delete event"})
