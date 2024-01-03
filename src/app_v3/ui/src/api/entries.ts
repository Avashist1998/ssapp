import { MessageRes } from "../types/api"
import { EntryBase, Entry } from "../types/datatypes"

const apiURL = "http://localhost:3000/entries/"

export async function getEntries() : Promise<Entry[]> {
    const res = await fetch(apiURL,  {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
    return res.json() as Promise<Entry[]>
}


export async function  getEntry(entry_id: number): Promise<Entry> {
    const res = await fetch(apiURL + entry_id, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
    return res.json() as Promise<Entry>
}

export async function addEntry(entry: EntryBase): Promise<Entry> {
    const res = await fetch(apiURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(entry)
    })
    return res.json() as Promise<Entry>
}

export async function deleteEntry (entry_id: number): Promise<MessageRes> {
    const res = await fetch(apiURL + entry_id.toString(), {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
    return res.json() as Promise<MessageRes>
}

