from os import getenv

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.data_service import DataService
from models import Player, Event, Entry


SQLITE_DB = getenv("SQLITE_DB_PATH", "database.db")
Base = declarative_base()
engine = create_engine(SQLITE_DB, connect_args={"check_same_thread": False})



class SqliteDS(DataService):
    """SQLITE DataStore implementation"""
    def __init__(self, engine: Engine, base: Base):
        """Constructor"""
        base.metadata.create_all(bind=engine)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        self.session = Session()
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


    def add_player(self, player: Player):
        """Add a player to the database"""
        try:

        except Exception as err:
            print("Error adding player to database", err)
    
    