import {useState, useEffect} from "react"
import { useNavigate, useLocation } from "react-router-dom"

import AddIcon from "@mui/icons-material/Add";
import SearchIcon from '@mui/icons-material/Search';
import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { Button, TextField, FormControlLabel, Checkbox, Box, CircularProgress } from "@mui/material";


import { addEvent, getEvents } from "../api/events"
import { SSEvent, SSEventBaseOptional } from "../types/datatypes"

import AddEventForm from "../forms/AddEventForm";
import EventsTable from "../components/EventsTable";
import MessageAlert from "../components/MessageAlert";



const EventsPage = () => {

    const [events, setEvents] = useState([] as SSEvent[]);
    const [totalEventsCount, setTotalEventsCount] = useState(0);
    const [reloadEvents, setReloadEvents] = useState(false);
    const [showAddEventForm, setShowAddEventForm] = useState(false);

    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    
    const offset = queryParams.get('offset') || '0';
    const limit = queryParams.get('limit') || '10';
    const creatorEmail = queryParams.get('creatorEmail') || "";
    const numOffset = Number(offset);
    const numLimit = Number(limit);
    
    const [isLoading, setIsLoading] = useState(true);
    const [eventsErrorMsg, setEventsErrorMsg] = useState("");

    const [isErrorMsg, setIsErrMsg] = useState(false);
    const [addEventMsg, setAddEventMsg] = useState("");
    const [eventLink, setEventLink] = useState<undefined | string>(undefined);

    useEffect(() => {
        getEvents({offset: numOffset, limit: numLimit}).then((res) => {
            if (res === undefined) {
                setEvents([]);
            } else {
                setEvents(res.events);
                setTotalEventsCount(res.count);
            }
            setReloadEvents(false);
        }).catch(() => {
            setEventsErrorMsg("API is currently down, please try again at a different time.")
        }).finally(() => {
            setIsLoading(false)
        });
      }, [reloadEvents, numLimit, numOffset, creatorEmail])


    const gotToEvent = (eventId: number) => {
        const path = `./${eventId}`;
        navigate(path);
    }

    const goToSignUp = () => {
        const path = "../signUp";
        navigate(path);
    }

    const onParamChange = (offset: number = 0, limit: number = 10, creatorEmail: string = "") => {
        console.log("creatorEmail: ", creatorEmail)
        let path = `${location.pathname}?`
        if (offset !== 0) {
            path = `${path}offset=${offset}&`
        }
        if (limit !== 10) {
            path = `${path}limit=${limit}&`
        }
        if (creatorEmail !== "") {
            path = `${path}creatorEmail=${creatorEmail}`
        }
        navigate(path);
    }

    const closeEventForm = () => {
        console.log(showAddEventForm);
        setShowAddEventForm(false);
        resetParameters();
    }

    const resetParameters = () => {
        setIsErrMsg(false);
        setAddEventMsg("");
        setEventsErrorMsg("");
    }

    const submitAddEvent = (event: SSEventBaseOptional) => {
        addEvent(event).then((res) => {
            if ('name' in res) {
                resetParameters()
                setAddEventMsg(`Event with name = "${res.name}" by user = "${res.creator}" has been created.`)
                setEventLink(`/${res.id.toString()}`)
            } else {
                setIsErrMsg(true);
                setAddEventMsg(res.message);
            }
            setReloadEvents(true);
        }).catch(() => {
            setIsErrMsg(true);
            setEventsErrorMsg("API is currently down, please try again at a different time.")
        })
    }


    if (isLoading) {
        return (
            <Box className="flex justify-center">
                <CircularProgress/>
            </Box>
        )
    }
    else if (eventsErrorMsg !== "") {   
        return (
            <MessageAlert isError={true} msg={eventsErrorMsg}/>
        )
    }
    else {
        return (
            <div className="p-[20px]">
                <div className="flex justify-end left-0">
                    <div className="mx-1">
                        <Button startIcon={<PersonAddAltIcon/>} variant="contained" color="primary" onClick={goToSignUp}>
                            Sign Up
                        </Button>
                    </div>
                    <div className="mx-1">
                        <Button startIcon={<AddIcon/>} variant="contained" color="success" onClick={()=> {setShowAddEventForm(true)}}>
                            Add Event
                        </Button>
                    </div>
                </div>
    
                <h1 className="justify-center flex p-4 text-8xl font-bold">Events Page</h1>
    
                { !showAddEventForm && 
                <>    
                    <div className="flex justify-center items-center my-2">
    
                            <TextField  id="searchText" variant="standard" />
                            <div className="mx-5">
                                <Button startIcon={<SearchIcon/>} variant="contained" color="success">
                                    Search
                                </Button>
                            </div>
                            <div>
                                <FormControlLabel control={<Checkbox defaultChecked />} label="Public" />
                            </div>
                            <div>
                                <FormControlLabel control={<Checkbox defaultChecked />} label="Private" />
                            </div>
    
                    </div>
                    <div className="flex justify-center items-center my-2">
                        <EventsTable events={events} totalCount={totalEventsCount} page={numOffset} rowPerPage={numLimit} navigateToEventPage={gotToEvent} onParamChange={onParamChange}/>
                    </div>
                </>
                } 
                { showAddEventForm && 
                    <AddEventForm onCloseForm={closeEventForm} submitEvent={submitAddEvent}>
                        <MessageAlert isError={isErrorMsg} msg={addEventMsg} link={eventLink}/>
                    </AddEventForm>
                }
            </div>
        )
    }
}

export default EventsPage