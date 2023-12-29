"""Player router"""
from models.player import PlayerBase
from fastapi import APIRouter, HTTPException, Request

from services.db_service import FailedToCreateException, FailedToGetException, FailedToDeleteException, FailedToUpdateException

router = APIRouter()

@router.get("/{player_email}")
async def get_player(request: Request, player_email: str):
    """Player endpoint"""
    try:
        player = request.app.db_service.get_player(request.app.db, player_email)
        if player is None:
            return HTTPException(status_code=404, detail=f"Player with {player_email=} does not exist")
        return player
    except FailedToGetException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to get player")
    except Exception as err:
        print(err)
        return HTTPException(status_code=500, detail="Player does not exist")


@router.post("/")
async def create_player(request: Request, player: PlayerBase):
    """Create player endpoint"""
    try:
        if request.app.db_service.get_player(request.app.db, player.email) is not None:
            return HTTPException(status_code=409, detail=f"Player with {player.email=} already exists")
        player = request.app.db_service.add_player(request.app.db, player)
        return player
    except FailedToCreateException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to create player")
    except Exception as _:
        return HTTPException(status_code=500, detail="Failed to create a player")

@router.put("/")
async def update_player(request: Request, player: PlayerBase):
    """Update event endpoint"""
    try:
        request.app.db_service.update_player(request.app.db, player)
        return {"message": "Player updated"}
    except FailedToUpdateException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to update player")
    except Exception as _:
        return HTTPException(status_code=500, detail="Failed to update player")


@router.delete("/{player_email}")
async def delete_event(request: Request, player_email: str):
    """Delete event endpoint"""
    try:
        request.app.db_service.delete_player(request.app.db, player_email)
        return {"message": "Player deleted"}
    except FailedToDeleteException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to delete player")
    except Exception as _:
        return HTTPException(status_code=500, detail="Failed to delete player")
