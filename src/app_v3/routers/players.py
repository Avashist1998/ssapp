"""Player router"""
from fastapi import APIRouter
from models import Player

router = APIRouter()

@router.get("/{player_email}")
async def get_player(player_email: str):
    """Player endpoint"""
    return {"event_id": player_email}


@router.post("/")
async def create_player(player: Player):
    """Create player endpoint"""
    print(player)
    return {"message": "Player created"}

@router.put("/{player_email}")
async def update_player(player_email: str, player: Player):
    """Update event endpoint"""
    print(player_email, player)
    return {"message": "Player updated"}

@router.delete("/{player_email}")
async def delete_event(player_email: str):
    """Delete event endpoint"""
    print(player_email)
    return {"message": "Player deleted"}
