"""Player router"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Path
from fastapi.responses import JSONResponse

from db.models import Player, PlayerBase, Message
from services.db_service import (
    FailedToCreateException,
    FailedToGetException,
    FailedToDeleteException,
    FailedToUpdateException,
)

router = APIRouter()


@router.get("/")
async def get_players(
    request: Request,
    offset: int = 0,
    limit: int = 10,
    player_name: Optional[str] = None,
):
    """Players endpoint"""
    offset = max(offset, 0)
    limit = max(limit, 10)
    limit = min(limit, 100)
    try:
        players = request.app.db_service.get_players(
            request.app.db, offset, limit, player_name
        )
        return players
    except FailedToGetException as err:
        print(err)
        return HTTPException(
            status_code=500, detail="Something went wrong with the database."
        )


@router.get("/{player_email}")
async def get_player(request: Request,
                     player_email: str = Path(...,
                                              description="The email of the player to get")):
    """Player endpoint"""
    try:
        player = request.app.db_service.get_player(request.app.db, player_email)
        if player is None:
            return HTTPException(
                status_code=404, detail=f"Player with {player_email=} does not exist"
            )
        return player
    except FailedToGetException as err:
        print(err)
        return HTTPException(
            status_code=500, detail="Something went wrong with the database."
        )


@router.post("/", response_model=Player, responses={409: {"model": Message}, 500: {"model": Message}})
async def create_player(request: Request, player: PlayerBase):
    """Create player endpoint"""
    try:
        db_player = request.app.db_service.get_player(request.app.db, player.email)
        if db_player:
            return JSONResponse(
                status_code=409, content={"message": f"Player with {player.email=} already exists"}
            )
        db_player = request.app.db_service.add_player(request.app.db, player)
        return db_player
    except FailedToCreateException as err:
        print(err)
        return JSONResponse(status_code=500, content={"message": "Failed to create player"})
    except Exception as _:
        return JSONResponse(status_code=500, content={"message": "Failed to create a player"})


@router.put("/")
async def update_player(request: Request, player: PlayerBase):
    """Update event endpoint"""
    try:
        db_player = request.app.db_service.get_player(request.app.db, player.email)
        if db_player is None:
            return HTTPException(
                status_code=404, detail=f"Player with {player.email=} does not exist"
            )
        request.app.db_service.update_player(request.app.db, player)
        return {"message": "Player updated"}
    except FailedToUpdateException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to update player")
    except Exception as _:
        return HTTPException(status_code=500, detail="Failed to update player")


@router.delete("/{player_email}")
async def delete_player(request: Request,
                        player_email: str = Path(...,
                                                 description="The email of the player to delete")):
    """Delete event endpoint"""
    try:
        db_player = request.app.db_service.get_player(request.app.db, player_email)
        if db_player is None:
            return HTTPException(
                status_code=404, detail=f"Player with {player_email=} does not exist"
            )
        request.app.db_service.delete_player(request.app.db, player_email)
        return {"message": "Player deleted"}
    except FailedToDeleteException as err:
        print(err)
        return HTTPException(status_code=500, detail="Failed to delete player")
    except Exception as _:
        return HTTPException(status_code=500, detail="Failed to delete player")
