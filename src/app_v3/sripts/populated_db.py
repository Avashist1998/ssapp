import requests
from app_v3.db.models import EventBase, PlayerBase, EntryBase


API_URL = "avashist.com"

players = [
    PlayerBase(name="Jerry Seinfeld", email="j_seinfeld@gmail.com"),
    PlayerBase(name="George Costanza", email="g_costanza@gmail.com"),
    PlayerBase(name="Cosmo Kramer", email="c_kramer@gmail.com"),
    PlayerBase(name="Elaine Benes", email="e_benes@gmail.com"),
    PlayerBase(name="Newman", email="newman@gmail.com")
]

events = [
    EventBase(name="Seinfeld Trivia Night", creator="j_seinfeld@gmail.com",
                location="Monk's Cafe", limit=5, price=5.00,
                rsvp_date="2021-04-01T00:00:00.000Z",
                event_date="2021-04-15T00:00:00.000Z"),
    EventBase(name="Yankees Game", creator="g_costanza@gmail.com", 
                location="Yankee Stadium", limit=3, price=50.00,
                rsvp_date="2021-04-01T00:00:00.000Z",
                event_date="2021-04-15T00:00:00.000Z"),
    EventBase(name="Kramer Dinner Party", creator="c_kramer@gmail.com",
                location="Kramer's Apartment", limit=8, price=0.00,
                rsvp_date="2021-04-01T00:00:00.000Z",
                event_date="2021-04-15T00:00:00.000Z"),
    EventBase(name="Elaine's Birthday", creator="e_benes@gmail.com",
                location="Elaine's Apartment", limit=20, price=0.00,
                rsvp_date="2021-04-01T00:00:00.000Z",
                event_date="2021-04-15T00:00:00.000Z"),
    EventBase(name="Newman's Birthday", creator="newman@gmail.com",
                location="Newman's Apartment", limit=5, price=0.00,
                rsvp_date="2021-04-01T00:00:00.000Z",
                event_date="2021-04-15T00:00:00.000Z"),
    EventBase(name="Elane's Boss Dinner", creator="e_benes@gmail.com",
                location="Chinese Restaurant", limit=5, price=0.00,
                rsvp_date="2021-04-01T00:00:00.000Z",
                event_date="2021-04-15T00:00:00.000Z")
]


entries = [
]



def clean_db():
    """Removes all the players, events, and entries from the database."""    
    for player in players:
        requests.delete(f"{API_URL}/players/{player.email}")




def populate_db():
    
    for player in players:
        requests.post(f"{API_URL}/players", json=player.dict())

    for event in events:
        requests.post(f"{API_URL}/events", json=event.dict())

    for entry in entries:
        requests.post(f"{API_URL}/entries", json=entry.dict())
