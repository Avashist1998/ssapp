"""Populates the database with players, events, and entries."""
import httpx
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from api.db.models import PlayerBase


# API_URL = "https://avashist.com"
API_URL = "http://localhost:3000"


@dataclass
class Event:
    """Event dataclass"""

    name: str
    creator: str
    location: str
    limit: int
    price: float
    rsvp_date: str
    event_date: str
    public: bool = True


players = [
    PlayerBase(name="Jerry Seinfeld", email="j_seinfeld@gmail.com"),
    PlayerBase(name="George Costanza", email="g_costanza@gmail.com"),
    PlayerBase(name="Cosmo Kramer", email="c_kramer@gmail.com"),
    PlayerBase(name="Elaine Benes", email="e_benes@gmail.com"),
    PlayerBase(name="Newman", email="newman@gmail.com"),
    PlayerBase(name="David Puddy", email="d_puddy@gmail.com"),
    PlayerBase(name="J. Peterman", email="j_peterman@gmail.com"),
]


def get_date_string(days: int) -> str:
    """Returns a date string in the format from today"""
    date = datetime.now() + timedelta(days=days)
    return date.strftime("%Y-%m-%dT00:00:00.000Z")


events = [
    Event(
        name="Seinfeld Trivia Night",
        creator="j_seinfeld@gmail.com",
        location="Monk's Cafe",
        limit=5,
        price=5.00,
        rsvp_date=get_date_string(2),
        event_date=get_date_string(5),
    ),
    Event(
        name="Yankees Game",
        creator="g_costanza@gmail.com",
        location="Yankee Stadium",
        limit=3,
        price=50.00,
        rsvp_date=get_date_string(3),
        event_date=get_date_string(7),
    ),
    Event(
        name="Kramer Dinner Party",
        creator="c_kramer@gmail.com",
        location="Kramer's Apartment",
        limit=8,
        price=0.00,
        rsvp_date=get_date_string(10),
        event_date=get_date_string(15),
    ),
    Event(
        name="Elaine's Birthday",
        creator="e_benes@gmail.com",
        location="Elaine's Apartment",
        limit=20,
        price=0.00,
        rsvp_date=get_date_string(1),
        event_date=get_date_string(12),
    ),
    Event(
        name="Newman's Birthday",
        creator="newman@gmail.com",
        location="Newman's Apartment",
        limit=5,
        price=0.00,
        rsvp_date=get_date_string(5),
        event_date=get_date_string(8),
    ),
    Event(
        name="Elane's Boss Dinner",
        creator="e_benes@gmail.com",
        location="Chinese Restaurant",
        limit=5,
        price=0.00,
        public=False,
        rsvp_date=get_date_string(3),
        event_date=get_date_string(8),
    ),
]

entries = {
    "Seinfeld Trivia Night": [
        "j_seinfeld@gmail.com",
        "g_costanza@gmail.com",
        "c_kramer@gmail.com",
        "e_benes@gmail.com",
    ],
    "Yankees Game": ["g_costanza@gmail.com", "c_kramer@gmail.com", "newman@gmail.com"],
    "Kramer Dinner Party": [
        "e_benes@gmail.com",
        "c_kramer@gmail.com",
        "d_puddy@gmail.com",
    ],
    "Elaine's Birthday": [
        "j_seinfeld@gmail.com",
        "g_costanza@gmail.com",
        "c_kramer@gmail.com",
    ],
    "Newman's Birthday": ["c_kramer@gmail.com"],
    "Elane's Boss Dinner": [
        "j_seinfeld@gmail.com",
        "g_costanza@gmail.com",
        "j_peterman@gmail.com",
    ],
}


def clean_db():
    """Removes all the players, events, and entries from the database."""

    for player in players:
        _ = httpx.delete(f"{API_URL}/players/{player.email}")


def populate_db():
    """Populates the database with players, events, and entries."""

    for player in players:
        res = httpx.post(f"{API_URL}/players/", json=player.model_dump())

    for event in events:
        res = httpx.post(f"{API_URL}/events/", json=asdict(event))
        for player_email in entries[event.name]:
            httpx.post(
                f"{API_URL}/entries/",
                json={
                    "event_id": res.json().get("id", ""),
                    "player_email": player_email,
                },
            )


def main():
    """Main function"""
    clean_db()
    populate_db()


if __name__ == "__main__":
    main()
