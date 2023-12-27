from typing import Optional, List
from fastapi import APIRouter, HTTPException

from models import Entry



router = APIRouter()

@router.get("/")
async def entries(event_id: Optional[str] = None, player_id: Optional[str] = None):
    """Entries endpoint"""

    if event_id is None and player_id is None:
        return HTTPException(status_code=403,
                      detail="Both event_id and player_id cannot be null at the same time")
    res_entry = Entry(_id="tmp", event_id="tmp", player_email="tmp@gmail.com")
    res:List[Entry] = [res_entry]
    if event_id and player_id:
        return res
    elif event_id:
        return res
    elif player_id:
        return res
    else:
        return HTTPException(status_code=500, detail="Something went wrong")


@router.post("/")
async def create_entry(entry: Entry):
    """Create entry endpoint"""
    print(create_entry)
    return {"message": "Entry created"}

@router.put("/{entry_id}")
async def update_entry(entry_id: str, entry: Entry):
    """Update entry endpoint"""
    print(entry_id, entry)
    return {"message": "Entry updated"}

@router.delete("/{entry_id}")
async def delete_entry(entry_id: str):
    """Delete entry endpoint"""
    print(entry_id)
    return {"message": "Entry deleted"}
