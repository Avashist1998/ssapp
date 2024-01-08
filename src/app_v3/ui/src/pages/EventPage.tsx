import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"

import { Box, Button, CircularProgress } from "@mui/material"
import ArticleIcon  from "@mui/icons-material/Article";
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';
import AddIcon from "@mui/icons-material/Add";


import { getEvent } from "../api/events"
import { addEntry } from "../api/entries";
import { SSEvent, EntryBase } from "../types/datatypes";

import AddEntryFrom from "../forms/AddEntryForm";
import EntriesList from "../components/EntriesList";
import MessageAlert from "../components/MessageAlert";


const EventPage = () => {

    const { eventId } = useParams<{eventId: string}>();
    const [reloadEvent, setReloadEvent] = useState(false);
    const [event, setEvent] = useState<SSEvent | null>(null)
 
    const [loading, setLoading] = useState(true);
    const [show404, setShow404] = useState(false);
    const [showEntryForm, setShowEntryForm] = useState(false);
    const [msg404, setMsg404] = useState("Page not found");

    const [errMsg, setErrMsg] = useState("");
    const [addedPlayerMsg, setAddedPlayerMsg] = useState("");

    const navigation = useNavigate();

    const gotToEventsPage = () => {
        const path = "../";
        navigation(path);
    }

    const submitAddEntry = (newEntry: EntryBase, callback: () => void) => {
        addEntry(newEntry).then((res) => {
            if ("id" in res) {
                setAddedPlayerMsg(`Player with email = ${res.player_email} has been added to event with id = ${res.event_id}`)
            } else {
                setErrMsg(res.message);
            }
        }).catch(() => {
            setErrMsg("Api is currently down, please try again at a different time.");
        }).finally(() => {
            setReloadEvent(true);
            callback();
        })
    }

    const closeForm = () => {
        setShowEntryForm(false);
        setErrMsg("");
        setAddedPlayerMsg("");
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
                <div className="flex justify-center m-2">
                    <div className="bg-slate-200 rounded-md px-[80px] py-[20px]" >
                        <h2 className="font-bold text-5xl p-2">{event?.name}</h2>
                        <h3 className="text-xl p-2"> Creator: {event?.creator}</h3>
                        <h3 className="text-xl p-2"> Location: {event?.location}</h3>
                        <h3 className="text-xl p-2"> People Limit: {event?.limit}</h3>
                        <h3 className="text-xl p-2"> Total RSVP: {event?.entries.length}</h3>
                        <h3 className="text-lg p-2">RSVP Date: {new Date(event?.rsvp_date || "").toLocaleDateString(undefined, {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            weekday: 'long',
                            })}</h3>
                        <h3 className="text-lg p-2">Event Date: {new Date(event?.event_date || "").toLocaleDateString(undefined, {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            weekday: 'long',
                            })}</h3>

                        <div className="flex justify-end left-0">
                            {event?.public ? <PublicIcon/> : <PublicOffIcon/>}
                            {event?.locked ? <LockIcon/> : <LockOpenIcon/>}
                        </div>
                    </div>
                </div>
                {showEntryForm ? 
                    <AddEntryFrom event_id= {Number(eventId)} submitAddEntry={submitAddEntry} closeForm={closeForm}>
                        <MessageAlert isError={errMsg !== ""} msg={errMsg === "" ? addedPlayerMsg : errMsg}/>
                    </AddEntryFrom> 
                    : 
                    <EntriesList entries={event?.entries || []}>
                        <div className="flex justify-end left-0">
                            <Button startIcon={<AddIcon/>} variant="contained" color="success" onClick={() => {setShowEntryForm(true)}} >
                                SignUp
                            </Button>
                        </div>
                    </EntriesList>
                    
                    }
            </div>
        )
        }
    }
}

export default EventPage;
  