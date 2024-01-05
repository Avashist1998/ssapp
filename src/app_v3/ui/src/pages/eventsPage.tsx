import { SSEvent, SSEventBaseOptional } from "../types/datatypes"
import {useState, useEffect} from "react"
import { useNavigate, useLocation } from "react-router-dom"

import AddIcon from "@mui/icons-material/Add";
import SearchIcon from '@mui/icons-material/Search';
import CancelIcon from '@mui/icons-material/Cancel';
import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import { Button, TextField, FormControlLabel, Checkbox, Box, CircularProgress } from "@mui/material";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TablePagination } from '@mui/material';
import Paper from '@mui/material/Paper';

import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import PublicIcon from '@mui/icons-material/Public';
import PublicOffIcon from '@mui/icons-material/PublicOff';

import { addEvent, getEvents } from "../api/events"

export function EventsTable ( props: {
    page: number,
    events: SSEvent[],
    rowPerPage: number,
    totalCount: number,
    navigateToEventPage: (eventId : number) => void,
    onPageAndRowPerPageChange: (page: number, rowPerPage: number) => void
  }) {

    const [page, setPage] = useState(props.page);
    const [rowsPerPage, setRowsPerPage] = useState(props.rowPerPage);


    useEffect(() => {
        console.log(page, rowsPerPage);
        props.onPageAndRowPerPageChange(page, rowsPerPage);
    }, [page, rowsPerPage])

    const handleChangePage = (
        event: React.MouseEvent<HTMLButtonElement> | null,
        newPage: number,
      ) => {
        console.log(event?.currentTarget.value);
        setPage(newPage);
    };


    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
      ) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
        
      };
    
    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell>Location</TableCell>
                        <TableCell>Creator</TableCell>
                        <TableCell>Locked</TableCell>
                        <TableCell>Public</TableCell>
                    </TableRow>
                </TableHead>

                <TableBody>
                {props.events.map((event) => {
                return (
                        <TableRow key={event.id} onClick={() => {
                            props.navigateToEventPage(event.id)
                        }}
                        
                        className="cursor-pointer hover:bg-slate-200">
                            <TableCell>{event.id}</TableCell>
                            <TableCell>{event.name}</TableCell>
                            <TableCell>{event.location}</TableCell>
                            <TableCell>{event.creator}</TableCell>
                            <TableCell>
                                { event.locked ? <LockIcon/> : <LockOpenIcon/>}
                            </TableCell>
                            <TableCell>{event.public ? <PublicIcon/> : <PublicOffIcon/>}</TableCell>
                        </TableRow>
                        ) 
                    })
                }
                </TableBody>

                <TablePagination
                    component="div"
                    count={props.totalCount}
                    page={page}
                    onPageChange={handleChangePage}
                    rowsPerPage={rowsPerPage}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                    />
            </Table>
        </TableContainer>

    )
  }


const EventsPage = () => {

    const [events, setEvents] = useState([] as SSEvent[]);
    const [totalEventsCount, setTotalEventsCount] = useState(0);
    const [reloadEvents, setReloadEvents] = useState(false);
    const [showAddEventForm, setShowAddEventForm] = useState(false);

    const [enableAddEvent, setEnableAddEvent] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
  
    const offset = queryParams.get('offset') || '0';
    const limit = queryParams.get('limit') || '10';
    const creatorEmail = queryParams.get('creatorEmail') || "";
    const numOffset = Number(offset);
    const numLimit = Number(limit);

    const [eventName, setEventName] = useState('');
    const [eventLocation, setEventLocation] = useState('');
    const [eventCreatorEmail, setEventCreatorEmail] = useState('');

    const [price, setPrice] = useState<null | number>(null);

    const [isPublic, setIsPublic] = useState(true);
    const [rsvpDate, setRSVPDate] = useState<Date | null>(null);

    const [eventLimit, setEventLimit] = useState<null | number>(null);
    const [eventDate, setEventDate] = useState<Date | null>(null);

    const [showErrMsg, setShowErrMsg] = useState(false);
    const [errMsg, setErrMsg] = useState("");

    useEffect(() => {
        console.log(creatorEmail);
        getEvents(numOffset, numLimit).then((res) => {

            if (res === undefined) {
                setEvents([]);
            } else {
                setEvents(res.events);
                setTotalEventsCount(res.count);
            }
            setIsLoading(false);
            setReloadEvents(false);
        }).catch(err => {
            console.log(err);
            setEvents([]);
        });

      }, [reloadEvents, numLimit, numOffset, creatorEmail])



    const getEventWithParams = (offset: number = 0, limit: number = 10) => {
        getEvents(offset, limit).then((res) => {
            if (res === undefined) {
                setEvents([]);
            } else {
                setEvents(res.events);
                setTotalEventsCount(res.count);
            }
            setIsLoading(false);
            setReloadEvents(false);
        }).catch(err => {
            console.log(err);
            setEvents([]);
        });
    }


    const gotToEvent = (eventId: number) => {
        const path = `./${eventId}`;
        navigate(path);
    }

    const goToSignUp = () => {
        const path = "../signUp";
        navigate(path);
    }
    // console.log(offset, limit)


    useEffect(() => {
        let val = true;
        if (eventName  == "") {
            val = val && false;
        }
        if (eventCreatorEmail == "") {
            val = val && false;
        }
        if (rsvpDate == null) {
            val = val && false;
        }
        if (eventDate == null) {
            val = val && false;
        }
        setEnableAddEvent(val);
    }, [eventName, eventCreatorEmail, eventLocation, price, eventLimit, isPublic, rsvpDate, eventDate])
    

    const resetParameters = () => {
        setPrice(0);
        setEventLimit(0);
        setEventName("");
        setIsPublic(true);
        setRSVPDate(null);
        setEventDate(null);
        setEventLocation("");
        setEventCreatorEmail("");
        setShowErrMsg(false);
        setErrMsg("");
    }

    const submitAddEvent = () => {

        let newEvent;
        if (rsvpDate !== null && eventDate !== null) {

            if (eventLimit === null && price === null) {
                newEvent = {
                    name: eventName,
                    location: eventLocation,
                    creator: eventCreatorEmail,
                    public: isPublic,
                    locked: false,
                    rsvp_date: rsvpDate.toISOString(),
                    event_date: eventDate.toISOString()
                } as SSEventBaseOptional
            } else if (eventLimit === null && price !== null) {
                newEvent= {
                    name: eventName,
                    location: eventLocation,
                    creator: eventCreatorEmail,
                    public: isPublic,
                    price: price,
                    locked: false,
                    rsvp_date: rsvpDate.toISOString(),
                    event_date: eventDate.toISOString()
                } as SSEventBaseOptional
            } else if (eventLimit !== null && price === null) {
                newEvent= {
                    name: eventName,
                    location: eventLocation,
                    creator: eventCreatorEmail,
                    public: isPublic,
                    limit: eventLimit,
                    locked: false,
                    rsvp_date: rsvpDate.toISOString(),
                    event_date: eventDate.toISOString()
                } as SSEventBaseOptional
            } else {
                newEvent= {
                    name: eventName,
                    location: eventLocation,
                    creator: eventCreatorEmail,
                    price: price,
                    limit: eventLimit,
                    public: isPublic,
                    locked: false,
                    rsvp_date: rsvpDate.toISOString(),
                    event_date: eventDate.toISOString()
                } as SSEventBaseOptional
            }
    
            addEvent(newEvent).then((res) => {
    
                if ('name' in res) {
                    console.log("This is where we log the error")
                    console.log(res)
                    resetParameters()
                    setShowAddEventForm(false); 
                    setEnableAddEvent(false);
                } else{
                    console.log("this is error")
                    console.log(res)
                    console.log(res.message);
                    setShowErrMsg(true);
                    setErrMsg(res.message);
                    setEnableAddEvent(false);
    
                }
                setReloadEvents(true);
            }).catch((err) => {
                console.log("this is were we are a catching")
                console.log(err)
            })
        }

    }

    if (isLoading) {
        return (
            <Box className="flex justify-center">
                <CircularProgress/>
            </Box>
        )
    }

    return(
        <div className="p-[20px]">
            <div className="flex justify-end left-0">
                <Button startIcon={<PersonAddAltIcon/>} variant="contained" color="primary" onClick={goToSignUp}>
                    Sign Up
                </Button>
                <Button startIcon={<AddIcon/>} variant="contained" color="success" onClick={()=> {setShowAddEventForm(true)}}>
                    Add Event
                </Button>
            </div>

            <h1 className="justify-center flex p-4 text-8xl font-bold">Events Page</h1>

            {!showAddEventForm && 
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
                    <EventsTable events={events} totalCount={totalEventsCount} page={numOffset} rowPerPage={numLimit} navigateToEventPage={gotToEvent} onPageAndRowPerPageChange={getEventWithParams}/>
                </div>

                {/* <h2>{numOffset} and {numLimit} and {creatorEmail}</h2> */}
            </>
            } 
            {showAddEventForm && 
            <>
                <div className="p-2 flex justify-center">
                    <div>
                        <div className="flex justify-end">
                            <Button onClick={() => {setShowAddEventForm(false)}} startIcon={<CancelIcon/>} variant="contained" color="error">
                                    Close
                            </Button>
                        </div>
                        <div>
                            <h2>Event Name:</h2>
                            <TextField id="eventName" label="Required" required onChange={e => setEventName(e.target.value)}/>
                        </div>
                        <div>
                            <h2>Creator Email</h2>
                            <TextField id="creatorEmail" label="Required" required onChange={e => setEventCreatorEmail(e.target.value)}/>
                        </div>
                        <div>
                        <h2>Location</h2>
                            <TextField id="location" onChange={e => setEventLocation(e.target.value)}/>
                        </div>
                        <div>
                            <h2>Price</h2>
                            <TextField id="price" type="number" value={price} onChange={e => setPrice(Number(e.target.value))}/>
                        </div>
                        <div>
                            <h2>Total People</h2>
                            <TextField id="limit" type="number" value={eventLimit} onChange={e => setEventLimit(Number(e.target.value))}/>
                        </div>
                        <div>
                            <FormControlLabel control={<Checkbox defaultChecked onChange={e => setIsPublic(e.target.checked)}/>} label="Public" />
                        </div>
                        <div>
                            <h2>RSVP Date</h2>
                            <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <DatePicker value={rsvpDate} onChange={val => setRSVPDate(val)}/>
                            </LocalizationProvider>
                        </div>
                        <div>
                            <h2>Event Date</h2>
                            <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <DatePicker value={eventDate} onChange={val => setEventDate(val)}
                                />
                            </LocalizationProvider>
                        </div>
                        <div className="flex justify-center">
                            <Button onClick={() => {submitAddEvent()}} startIcon={<AddIcon/>} disabled={!enableAddEvent} color="success">
                                Add Event
                            </Button>
                        </div>
                        <div>
                            {showErrMsg && 
                            <>
                                <h2>{errMsg}</h2>
                            </>
                            }
                        </div>
                    </div>
                </div>
            </>


            }
        </div>
    )
}


export default EventsPage