"""SQLITE DataStore implementation"""
from typing import Any, Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from db.models import Entry, EntryBase, Player, PlayerBase, Event, EventBase
from db.schema import PlayerORM, EventORM, EntryORM
from services.db_service.utils import (
    FailedToCreateException,
    FailedToGetException,
    FailedToDeleteException,
    FailedToUpdateException,
    FailedDataServiceException,
)


class SqliteService:
    """SQLITE DataStore implementation"""

    def __init__(self):
        """Constructor"""
        self.name = "sql alchemy tool"

    def get_players(
        self,
        db: Session,
        offset: int = 1,
        limit: int = 10,
        player_name: Optional[str] = None,
    ) -> List[Player]:
        """Get all players from the database"""
        try:
            db_players = (
                db.query(PlayerORM).offset((offset - 1) * limit).limit(limit).all()
            )
            if player_name:
                db_players = (
                    db.query(PlayerORM)
                    .filter(PlayerORM.name.like(player_name))
                    .offset((offset - 1) * limit)
                    .limit(limit)
                    .all()
                )
            db.commit()
            return [Player.model_validate(db_player) for db_player in db_players]
        except SQLAlchemyError as err:
            print(err)
            raise FailedToGetException("Failed to get players") from err
        except Exception as err:
            print(err)
            print("Error getting players to database", err)

    def add_player(self, db: Session, player: PlayerBase) -> Optional[Player]:
        """Add a player to the database"""
        try:
            db_player = PlayerORM(email=player.email, name=player.name)
            db.add(db_player)
            db.commit()
            db.refresh(db_player)
            print(db_player)
            return Player.model_validate(db_player)
        except SQLAlchemyError as err:
            raise FailedDataServiceException("Failed to create player") from err
        except Exception as err:
            print("Something went wrong", err)

    def get_player(self, db: Session, email: str) -> Player:
        """Get a player from the database"""
        try:
            db_player = db.query(PlayerORM).filter(PlayerORM.email == email).first()
            db.commit()
            if db_player is None:
                return None
            db.refresh(db_player)
            return Player.model_validate(db_player)
        except SQLAlchemyError as err:
            print(err)
            raise FailedToGetException("Failed to get player") from err
        except Exception as err:
            print(f"Error getting player to database with {email=}", err)

    def delete_player(self, db: Session, email: str) -> Player:
        """Deletes the player from database"""
        try:
            player_deleted_count = (
                db.query(PlayerORM).filter(PlayerORM.email == email).delete()
            )
            db.commit()
            if player_deleted_count == 0:
                raise SQLAlchemyError("Failed to find player to delete")
        except SQLAlchemyError as err:
            raise FailedToDeleteException("Failed to delete player") from err
        except Exception as err:
            print(f"Error removing player form database with {email=}", err)

    def update_player(self, db: Session, player: Player):
        """Update a player in the database"""
        try:
            update_count = (
                db.query(PlayerORM)
                .filter(PlayerORM.email == player.email)
                .update({"name": player.name})
            )
            db.commit()
            if update_count == 0:
                raise SQLAlchemyError("Failed to find player to update")
        except SQLAlchemyError as err:
            raise FailedToUpdateException("Failed to update player") from err
        except Exception as err:
            print(f"Error updating player in database with {player.email=}", err)

    def get_events(
        self,
        db: Session,
        offset: int = 1,
        limit: int = 10,
        creator_email: Optional[str] = None,
        public: Optional[bool] = None,
    ) -> Tuple[int, List[Event]]:
        """Get all events from the database"""
        try:
            total_count = db.query(EventORM).count()
            print(f"total number of events in db = {total_count}")
            # print(
            #     db.query(EventORM)
            #     .offset(offset - 1 * limit)
            #     .limit(limit)
            #     .count()
            # )
            db_events = (
                db.query(EventORM)
                .offset((offset - 1) * limit)
                .limit(limit)
                .all()
            )
            if public:
                db_events = (
                    db.query(EventORM)
                    .filter(EventORM.public == public)
                    .offset((offset - 1) * limit)
                    .limit(limit)
                    .all()
                )
            if creator_email:
                print(creator_email)
                db_events = (
                    db.query(EventORM)
                    .filter(EventORM.creator == creator_email)
                    .filter(EventORM.public == public)
                    .offset((offset - 1) * limit)
                    .limit(limit)
                    .all()
                )
            if creator_email and public:
                db_events = (
                    db.query(EventORM)
                    .filter(EventORM.creator == creator_email)
                    .filter(EventORM.public == public)
                    .offset((offset - 1) * limit)
                    .limit(limit)
                    .all()
                )
            db.commit()
            print(db_events)
            return total_count, [Event.model_validate(db_event) for db_event in db_events]
        except SQLAlchemyError as err:
            print(err)
            raise FailedToGetException("Failed to get events") from err
        except Exception as err:
            print(err)
            print(f"Error getting events to database", err)

    def add_event(self, db: Session, event: EventBase) -> Event:
        """Add a event to the database"""
        try:
            db_event = EventORM(
                name=event.name,
                creator=event.creator,
                location=event.location,
                limit=event.limit,
                price=event.price,
                public=event.public,
                locked=event.locked,
                rsvp_date=event.rsvp_date,
                event_date=event.event_date,
            )
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return Event.model_validate(db_event)
        except SQLAlchemyError as err:
            raise FailedToCreateException("Failed to create event") from err
        except Exception as err:
            print(err)
            print("Something went wrong", err)

    def get_event(self, db: Session, _id: int) -> Optional[Event]:
        """Get a event from the database"""
        try:
            print(f"total number of events in db = {db.query(EventORM).count()}")
            db_event = db.query(EventORM).filter(EventORM.id == int(_id)).first()
            db.commit()
            if db_event is None:
                return None
            return Event.model_validate(db_event)
        except SQLAlchemyError as err:
            print(err)
            raise FailedToGetException("Failed to get event") from err
        except Exception as err:
            print(err)
            print(f"Error getting event to database with {id=}", err)

    def delete_event(self, db: Session, _id: int):
        """Deletes the event from database"""
        try:
            event_deleted_count = db.query(EventORM).filter(EventORM.id == _id).delete()
            db.commit()
            if event_deleted_count == 0:
                raise SQLAlchemyError("Failed to find event to delete")
        except SQLAlchemyError as err:
            raise FailedToDeleteException("Failed to delete event") from err
        except Exception as err:
            print(f"Error removing event form database with {id=}", err)

    def update_event(self, db: Session, event: Event):
        """Update a event in the database"""
        try:
            update_event_count = (
                db.query(EventORM)
                .filter(EventORM.id == event.id)
                .update(
                    {
                        "name": event.name,
                        "location": event.location,
                        "limit": event.limit,
                        "price": event.price,
                        "public": event.public,
                        "locked": event.locked,
                        "rsvp_date": event.rsvp_date,
                        "event_date": event.event_date,
                    }
                )
            )
            db.commit()
            if update_event_count == 0:
                raise SQLAlchemyError("Failed to find event to update")
        except SQLAlchemyError as err:
            raise FailedToUpdateException("Failed to update event") from err
        except Exception as err:
            print(f"Error updating event in database with {event.id=}", err)

    def get_entries(
        self,
        db: Session,
        player_email: Optional[str] = None,
        event_id: Optional[int] = None,
        offset: int = 1,
        limit: int = 10,
    ) -> List[Entry]:
        """Get all entries from the database"""
        try:
            db_entries = (
                db.query(EntryORM).offset((offset-1)*limit).limit(limit).all()
            )
            if player_email:
                db_entries = (
                    db.query(EntryORM)
                    .filter(EntryORM.player_email == player_email)
                    .offset((offset-1)*limit).limit(limit)
                    .all()
                )
            if event_id:
                db_entries = (
                    db.query(EntryORM)
                    .filter(EntryORM.event_id == event_id)
                    .offset((offset-1)*limit).limit(limit)
                    .all()
                )
            if player_email and event_id:
                db_entries = (
                    db.query(EntryORM)
                    .filter(EntryORM.player_email == player_email)
                    .filter(EntryORM.event_id == event_id)
                    .offset((offset-1)*limit).limit(limit)
                    .all()
                )
            db.commit()
            return [Entry.model_validate(db_entry) for db_entry in db_entries]
        except SQLAlchemyError as err:
            print(err)
            raise FailedToGetException("Failed to get entries") from err
        except Exception as err:
            print(err)
            print("Error getting entries to database", err)

    def add_entry(self, db: Session, entry: EntryBase) -> Entry:
        """Create a entry in the database"""
        try:
            db_entry = EntryORM(
                event_id = entry.event_id,
                player_email=entry.player_email,
            )
            db.add(db_entry)
            db.commit()
            print(db_entry.id)
            print(db_entry)
            db.refresh(db_entry)
            return Entry.model_validate(db_entry)
        except SQLAlchemyError as err:
            raise FailedToCreateException("Failed to create entry") from err
        except Exception as err:
            print(err)
            print("Something went wrong", err)

    def get_entry(self, db: Session, _id: int) -> Optional[Entry]:
        """Get a entry from the database"""
        try:
            db_entry = db.query(EntryORM).filter(EntryORM.id == _id).first()
            db.commit()
            if db_entry is None:
                return None
            return Entry.model_validate(db_entry)
        except SQLAlchemyError as err:
            raise FailedToGetException("Failed to get entry") from err
        except Exception as err:
            print(err)
            print("Something went wrong", err)

    def delete_entry(self, db: Session, _id: int):
        """Deletes the entry from database"""
        try:
            _ = db.query(EntryORM).filter(EntryORM.id == _id).delete()
            db.commit()
        except SQLAlchemyError as err:
            raise FailedToDeleteException("Failed to delete entry") from err
        except Exception as err:
            print(err)
            print("Something went wrong", err)
