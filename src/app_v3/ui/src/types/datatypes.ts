export type SSEvent = {
    id: number,
    name: string,
    creator: string,
    location: string,
    limit: number,
    price: number,
    public: boolean,
    locked: boolean,
    rsvp_date: string,
    event_date: string,
    created_date: string,
    entries: Array<Entry>
}

export type Message = {
    message: string
}

export type SSEventBase = {
    name: string,
    creator: string,
    location: string,
    limit: number,
    price: number,
    public: boolean,
    locked: boolean,
    rsvp_date: string,
    event_date: string,
}

export type SSEventBaseOptional = Partial<Pick<SSEventBase, 'location' | 'limit'>> & Omit<SSEventBase, 'location' | 'limit'>;

// export type Entry = {
//     id: number
//     event_id: number
//     player_email: string
//     created_date: string
// }

export type Player = {
    name: string,
    email: string,
    created_date: string,
    entries: Array<Entry>
}

export type PlayerBase = {
    name: string,
    email: string
}

export type Entry =  {
    id: number,
    event_id: number,
    ss_email: null | string,
    player_email: string,
    created_date: string,
}

export type EntryBase = {
    event_id: number,
    player_email: string
}