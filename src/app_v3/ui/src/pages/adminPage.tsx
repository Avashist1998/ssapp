import { FormEvent, useEffect, useState } from 'react'


import { addEntry, getEntries, deleteEntry } from '../api/entries'
import { addPlayer, getPlayers, deletePlayer } from "../api/players"
import { getEvents, deleteEvent, addEvent } from "../api/events"
import { SSEvent, PlayerBase, Player, Entry, EntryBase, SSEventBaseOptional } from "../types/datatypes"


function stringifyDate(inputDate: string): string {

  const date = new Date(inputDate);
  const isoString = date.toISOString();
  return isoString;
}


function AddEventForm (props: {
  addEvent: (event: SSEventBaseOptional) => void
}) {

  const [errorMessage, setErrorMessage] = useState("");
  const [showErrorMsg, setShowErrMsg] = useState(false);

  const [newEvent, setNewEvent] = useState<SSEventBaseOptional>(
    {
      name: "",
      creator: "",
      price: 0,
      public: true,
      locked: false,
      rsvp_date: "",
      event_date: "",
    }
  )
  function handleSummit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (newEvent.name === "") {
      setErrorMessage("Event name cannot be empty.");
      setShowErrMsg(true);
    }
    else if (newEvent.creator === "") {
      setErrorMessage("Event creator email cannot be empty.");
      setShowErrMsg(true);
    } else {
      props.addEvent(newEvent)
    }
  }
  return (
    <div className="p-[10px]">
    <h3> Add the Event </h3>
    <form onSubmit={handleSummit}>
      <div>
        <label>
          Name:
        </label>
        <input type="text" name="name" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            name: e.currentTarget.value
          }))
        }}/>
      </div>
      <div>
        <label>
          Creator email:
        </label>
        <input type="text" name="creatorEmail" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            email: e.currentTarget.value
          }))
        }}/>
      </div>
      <div>
        <label>
          location
        </label>
        <input type="text" name="location" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            location: e.currentTarget.value
          }))
        }} />
      </div>
      <div>
        <label>
          price
        </label>
        <input type="number" name="price" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            price: Number(e.currentTarget.value)
          }))
         }} />
      </div>
      <div>
        <label>
          limit
        </label>
        <input type="number" name="limit" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            limit: Number(e.currentTarget.value)
          }))
        }}/>
      </div>
      <div>
        <label>
          Public
        </label>
        <input type="checkbox" name="public" value={newEvent.public ? "on" : "off"} onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            public: e.currentTarget.value === "on"
          }))
        }}/>
      </div>
      <div>
        <label>
          RSVP date
        </label>
        <input type="date" name="rsvpDate" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            rsvp_date: stringifyDate(e.currentTarget.value as string)
          }))
        }}
      />
      </div>
      <div>
        <label>
          Event date
        </label>
        <input type="date" name="eventDate" onChange={e => {
          setNewEvent((prevState) => ({
            ...prevState,
            event_date: stringifyDate(e.currentTarget.value as string)
          }))
        }}
      />
      </div>
      {showErrorMsg && <h4 className="text-red-700">{errorMessage}</h4>}
      <input type="submit" value="Submit" />
    </form>
    </div>
  )
}


function AddEntryForm (props: {
  addEntry: (entry: EntryBase) => void
}) {

  const[newEntry, setNewEntry] = useState({
    event_id: -1,
    player_email: ""
  } as EntryBase)

  function handleSummit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (newEntry.event_id === undefined) {
      console.log("can not Submit an Empty name")
    }
    else if (newEntry.player_email === "") {
      console.log("Can not Submit an Empty Email")
    } else {
      props.addEntry(newEntry)
    }
  }
  return (
    <div className="p-[10px]">
    <h3> Add the player </h3>
    <form onSubmit={handleSummit}>
      <div>
        <label>
          Event ID:
        </label>
        <input type="number" name="event_id" onChange={e => {
          setNewEntry((prevState) => ({
            ...prevState,
            event_id : Number(e.currentTarget.value)
          }))
        }} />
      </div>
      <div>
        <label>
          Your Email:
        </label>
        <input type="text" name="email" onChange={e => {
          setNewEntry((prevState) => ({
            ...prevState,
            player_email : e.currentTarget.value
          }))
        }} />
      </div>
      <input type="submit" value="Submit" />
    </form>
    </div>
  )
}

function AddPlayerForm (props: {
  addPlayer: (player: PlayerBase) => void
}) {

  const [newPlayer, setNewPlayer]= useState<PlayerBase>({
    name: "",
    email: ""
  })

  function handleSummit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (newPlayer.name === "") {
      console.log("can not Submit an Empty name")
    }
    else if (newPlayer.email === "") {
      console.log("Can not Submit an Empty Email")
    } else {

      props.addPlayer(newPlayer)
    }
  }
  return (
    <div className="p-[10px]">
    <h3> Add the player </h3>
    <form onSubmit={handleSummit}>
      <div>
        <label>
          Name:
        </label>
        <input type="text" name="name" onChange={e => {
          setNewPlayer(prevState => ({
            ...prevState,
            name: e.currentTarget.value
          }))
        }}/>
      </div>
      <div>
        <label>
          Email:
        </label>
        <input type="text" name="email" onChange={e => {
          setNewPlayer(prevState => ({
            ...prevState,
            email: e.currentTarget.value
          }))
        }}/>
      </div>
      <input type="submit" value="Submit" />
    </form>
    </div>
  )
}

function EntriesTable (props: {
  entries: Entry[],
  removeEntry: (entry_id: number) => void
}) {
  return (
    <div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Event ID</th>
          <th>Player Email</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
      {props.entries.map((entry) => {
        return (
          <tr key={entry.id}>
              <td>{entry.id}</td>
              <td>{entry.event_id}</td>
              <td>{entry.player_email}</td>
              <td><button onClick={() => {
                props.removeEntry(entry.id)
              }}>x</button></td>
          </tr>
        ) 
      })
      }
      </tbody>
    </table>
    </div>
  )
}


function PlayersTable ( props: {
  players: Player[],
  removePlayer: (player_email: string) => void
}) {
 
  return (
    <div>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
      {props.players.map((player) => {
        return (
          <tr key={player.email}>
              <td>{player.name}</td>
              <td>{player.email}</td>
              <td><button onClick={() => {
                props.removePlayer(player.email)
                console.log(player)
              }}>x</button></td>
          </tr>
        ) 
      })
      }
      </tbody>
    </table>
    </div>
  )
}


export function EventsTable ( props: {
  events: SSEvent[],
  removeEvent: (event_id: number) => void
}) {
 
  return (
    <div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Creator</th>
          <th>Locked</th>
          <th>Public</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
      {props.events.map((event) => {
        return (
          <tr key={event.id}>
              <td>{event.id}</td>
              <td>{event.name}</td>
              <td>{event.location}</td>
              <td>{event.creator}</td>
              <td>{event.locked.toString()}</td>
              <td>{event.public.toString()}</td>
              <td><button onClick={() => {
                props.removeEvent(event.id)

              }}>x</button></td>
          </tr>
        ) 
      })
      }
      </tbody>
    </table>
    </div>
  )
}


function AdminPage() {
    const [reloadEvents, setReloadEvents] = useState(false);
    const [showEventForm, setShowEventForm] = useState(false);
    const [eventButtonText, setEventButtonText] = useState("Add Event");
  
    const [reloadPlayers, setReloadPlayers] = useState(false);
    const [showPlayerForm, setShowPlayerForm] = useState(false);
    const [playerButtonText, setPlayerButtonText] = useState("Add Player");
  
    const [reloadEntries, setReloadEntries] = useState(false);
    const [showEntryForm, setShowEntryForm] = useState(false);
    const [entryButtonText, setEntryButtonText] = useState("Add Entry");
    
    const [entries, setEntries] = useState([] as Entry[]);
    const [players, setPlayers] = useState([] as Player[]);
  
    const [events, setEvents] = useState([] as SSEvent[]);
  
    useEffect(() => {
      getEvents().then((res) => {
        setEvents(res.events)
      });
      setReloadEvents(false);
    }, [reloadEvents])
  
    useEffect(() => {
      getPlayers().then((players) => {
        setPlayers(players)
      })
      setReloadPlayers(false);
    }, [reloadPlayers])
  
    useEffect(() => {
      getEntries().then((entries) => {
        setEntries(entries)
      })
      setReloadEntries(false);
    }, [reloadEntries])
  
    function removeEvent (id: number): void {
      deleteEvent(id)
      setReloadEvents(true);
    }
  
    function removePlayer (player_email: string): void {
      deletePlayer(player_email)
      setReloadPlayers(true)
    }
  
    function removeEntry (entry_id: number): void {
      deleteEntry(entry_id).then(() => {
        setReloadEntries(true);
      });
    }
  
    function submitEvent (event: SSEventBaseOptional): void {
      addEvent(event);
      setEventButtonText("Add Event")
      setShowEventForm(false)
      setReloadEvents(true)
    }
  
    function submitPlayer (player: PlayerBase): void {
      addPlayer(player)
      setPlayerButtonText("Add Player")
      setShowPlayerForm(false)
      setReloadPlayers(true)
    }
  
    function submitEntry (entry: EntryBase): void {
      addEntry(entry)
      setEntryButtonText("Add Entry")
      setShowEntryForm(false)
      setReloadEntries(true)
    }
    
    return (

        <div>
        <div className="p-2 justify-center">
          <button className="bg-green-300 hover:bg-green-500 m-2" onClick={() => {
              if (!showPlayerForm) {
              setPlayerButtonText("Close Player Form")
              setShowPlayerForm(true)
              } else {
              setPlayerButtonText("Add Player")
              setShowPlayerForm(false)
              }
          }}>
              {playerButtonText} 
          </button>
          <button className="bg-green-300 hover:bg-green-500 m-2" onClick={() => {
            if (!showEventForm) {
            setEventButtonText("Close Event Form")
            setShowEventForm(true)
            } else {
            setEventButtonText("Add Event")
            setShowEventForm(false)
            }
        }}>
            {eventButtonText} 
        </button>
          <button className="bg-green-300 hover:bg-green-500 m-2" onClick={() => {
            if (!showEntryForm) {
            setEntryButtonText("Close Entry Form")
            setShowEntryForm(true)
            } else {
            setEntryButtonText("Add Entry")
            setShowEntryForm(false)
            }
        }}>
            {entryButtonText} 
        </button>
        </div>
        <h1 className="justify-center flex">SS Players!</h1>


        {
        showPlayerForm && <AddPlayerForm  addPlayer={submitPlayer}/>
        }

        <PlayersTable players={players} removePlayer={removePlayer} />
        <h1>SS Events!</h1>
        {
        showEventForm && <AddEventForm  addEvent={submitEvent}/>
        }

        <EventsTable events={events} removeEvent={removeEvent}/>

        <h1>SS Entries!</h1>
        {
        showEntryForm && <AddEntryForm  addEntry={submitEntry}/>
        }

        <EntriesTable entries={entries} removeEntry={removeEntry}/>
        </div>
    )
}


export default AdminPage;