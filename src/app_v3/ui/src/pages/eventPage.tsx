import { getEvent } from "../api/events"
import { useEffect, useState } from "react";
import { SSEvent, Entry, EntryBase } from "../types/datatypes";

import { useParams, useNavigate } from "react-router-dom"
import {Box, Button, CircularProgress, List, ListItem, ListItemText, TextField } from "@mui/material"
import ArticleIcon  from "@mui/icons-material/Article";
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';
import AddIcon from "@mui/icons-material/Add";
import CancelIcon from "@mui/icons-material/Cancel";
import { addEntry } from "../api/entries";


const EntriesList = ( props : {
    entries: Entry[],
    setShowEntryForm:  React.Dispatch<React.SetStateAction<boolean>>
}) => {

    return (
        <>
            <div className="flex justify-end left-0">
                <Button startIcon={<AddIcon/>} variant="contained" color="success" onClick={() => {props.setShowEntryForm(true)}} >
                    SignUp
                </Button>
            </div>
            <div className="flex justify-center">
                <h1  className="text-2xl font-bold">Players</h1>
            </div>
            <div className="flex justify-center">
                <List>
                    {props.entries.map((entry) => {
                    return (
                        <ListItem key={entry.id}>
                            <ListItemText primary={entry.player_email} secondary={entry.created_date}/>
                        </ListItem>
                        )
                    })
                }
                </List>
            </div>
        </>

    )
}


const EntrySignUpForm = (props: {
    eventId: number,
    addEntry: (entry: EntryBase) => void,
    setReloadEvent: React.Dispatch<React.SetStateAction<boolean>>,
    setShowAddEntryForm: React.Dispatch<React.SetStateAction<boolean>>
}) => {

    const [enableAddEvent, setEnableAddEvent] = useState(false);
    const [eventPlayerEmail, setEventPlayerEmail] = useState("");

    const [isAddingEvent, setIsAddingEvent] = useState(false);
    const [errMsg, setErrMsg] = useState("");

    useEffect(() => {
        let val = true;
        if (eventPlayerEmail === "") {
            val = val && false;
        }
        if (!eventPlayerEmail.includes("@")) {
            val = val && false;
        } 
        if (!eventPlayerEmail.includes(".")) {
            val = val && false;
        }
        setEnableAddEvent(val);
    }, [eventPlayerEmail])

    const submitAddEntry = () => {
        const newEntry = {
            event_id: props.eventId,
            player_email:  eventPlayerEmail
        } as EntryBase;
        setIsAddingEvent(true);
        addEntry(newEntry).then((res) => {
            if ("id" in res) {
                console.log(res);
                setIsAddingEvent(false);
                setEventPlayerEmail("");
                props.setReloadEvent(true);
                props.setShowAddEntryForm(false);
            } else {
                console.log("this was triggered")
                setIsAddingEvent(false);
                setEventPlayerEmail("");
                setErrMsg(res.message);
            }
        }).catch(err => {
            console.log(err);
            setIsAddingEvent(false);
            setErrMsg("An error occurred while adding the player");
        })
    }
    return (
        <div>
            <div className="flex justify-end">
                <Button onClick={() => {props.setShowAddEntryForm(false)}} startIcon={<CancelIcon/>} variant="contained" color="error">
                        Close
                </Button>
            </div>

            {isAddingEvent ? 
            <Box className="flex justify-center">
                <CircularProgress/>
            </Box>
            :
            <> 
                <div className="justify-center flex">
                    <h1 className="text-2xl font-bold justify-center flex">Add Player</h1>
                </div>
                <div className="justify-center flex">
                    <div>
                        <div>
                            <h2>Player Email</h2>
                            <TextField id="creatorEmail" label="Required" required onChange={e => setEventPlayerEmail(e.target.value)}/>
                        </div>
                    </div>
                </div>
                <div className="flex justify-center py-2">
                    <Button onClick={() => {submitAddEntry()}} startIcon={<AddIcon/>} color="success" variant="contained" disabled={!enableAddEvent}>
                        Add Event
                    </Button>
                </div>
                {
                    errMsg !== "" &&
                    <div className="flex justify-center">
                        <h3>
                            {errMsg}
                        </h3>
                    </div>
                }
            </>
            }

        </div> 
    );
}

const EventPage = () => {

    const { eventId } = useParams<{eventId: string}>();
    const [reloadEvent, setReloadEvent] = useState(false);
    const [event, setEvent] = useState<SSEvent | null>(null)
 
    const [loading, setLoading] = useState(true);
    const [show404, setShow404] = useState(false);
    const [showEntryForm, setShowEntryForm] = useState(false);
    const [msg404, setMsg404] = useState("Page not found");
    const navigation = useNavigate();

    const gotToEventsPage = () => {
        const path = "../";
        navigation(path);
    }

    const SignUpForEvent = (entry: EntryBase) => {
        console.log(entry);
    }

    useEffect(() => {
        if (eventId === undefined) {
        setShow404(true)
        } else {
        getEvent(eventId).then((res) => {
            if ("id" in res) {
                setEvent(res);
                setLoading(false)
                setReloadEvent(false);
            } else {
                setShow404(true)
                setLoading(false)
                setMsg404(res.message)
            }
        }).catch((err) => {
            console.log("and error occurred")
            console.log(err);
            setShow404(true);
            setReloadEvent(false);
        })
        }
    }, [eventId, reloadEvent])

    if (loading) {
        return (
        <Box className="flex justify-center">
            <CircularProgress/>
        </Box>
        )
    } else {
        if (show404) {
        return (
            <div>
                <h1 className="flex justify-center pt-[50px] font-bold text-6xl">404</h1>
                <h2 className="flex justify-center pt-[50px] font-bold text-3xl">{msg404}</h2> 
            </div>
        )
        } else {
        return (
            <div className="p-[20px]">
                <div className="flex justify-end left-0">
                    <Button startIcon={<ArticleIcon/>} variant="contained" color="primary" onClick={gotToEventsPage}>
                        Events
                    </Button>
                </div>
                <div className="flex justify-center">
                    <div className="bg-slate-200 rounded-md px-[80px] py-[20px]" >
                        <h2 className="font-bold text-5xl p-2">{event?.name}</h2>
                        <h3 className="text-xl p-2"> Creator: {event?.creator}</h3>
                        <h3 className="text-xl p-2"> Location: {event?.location}</h3>
                        <h3 className="text-xl p-2"> People Limit: {event?.limit === null}</h3>
                        <h3 className="text-xl p-2"> Total RSVP: {event?.entries.length}</h3>
                        <h3 className="text-lg p-2">RSVP Date: {new Date(event?.rsvp_date || "").toLocaleDateString()}</h3>
                        <h3 className="text-lg p-2">Event Date: {new Date(event?.event_date || "").toLocaleDateString()}</h3>

                        <div className="flex justify-end left-0">
                            {event?.public ? <PublicIcon/> : <PublicOffIcon/>}
                            {event?.locked ? <LockIcon/> : <LockOpenIcon/>}
                        </div>
                    </div>
                </div>
                {showEntryForm ? <EntrySignUpForm eventId={Number(eventId)} addEntry={SignUpForEvent} setShowAddEntryForm={setShowEntryForm} setReloadEvent={setReloadEvent}/> : <EntriesList entries={event?.entries || []} setShowEntryForm={setShowEntryForm}/>}
            </div>
        )
        }
    }
}

export default EventPage;
  