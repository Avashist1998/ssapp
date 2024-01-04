import { apiURL } from "./base"
import { MessageRes, EventsRes } from "../types/api"
import { SSEvent, Message, SSEventBaseOptional } from "../types/datatypes"

const eventsApiURL = `${apiURL}/events/`


export async function  getEvents(offset: number = 1, limit: number = 10): Promise<EventsRes> {
    const res = await fetch(`${eventsApiURL}?limit=${limit}&offset=${offset}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })

    return res.json() as Promise<EventsRes>
}


export async function deleteEvent (event_id: number): Promise<MessageRes> {
    const res = await fetch(eventsApiURL  + event_id.toString(), {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
    return res.json() as Promise<MessageRes>
}



export async function addEvent(event: SSEventBaseOptional): Promise<SSEvent | Message> {
    try{
        const res = await fetch(eventsApiURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(event)
        })

        if (!res.ok) {
            return res.json() as Promise<Message>
        }
        return res.json() as Promise<SSEvent>
    } catch (error) {
        console.error("An error occurred while adding the event:", error)
        throw error;
    }
}


export async function getEvent(event_id: string): Promise<SSEvent| Message> {
    const res = await fetch(eventsApiURL +  event_id.toString(),
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        } 
    )
    if (!res.ok) {
        return res.json() as Promise<Message>
    }
    return res.json() as Promise<SSEvent>
}