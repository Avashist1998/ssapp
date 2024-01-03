import { MessageRes } from "../types/api"
import { Player, PlayerBase } from "../types/datatypes"

const apiURL = "http://localhost:3000/players/"

export async function getPlayers() : Promise<Player[]> {
    const res = await fetch(apiURL,  {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
    return res.json() as Promise<Player[]>
}


export async function  getPlayer(email: string): Promise<Player> {
    const res = await fetch(apiURL + email, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
    return res.json() as Promise<Player>
}

export async function addPlayer(player: PlayerBase): Promise<Player> {
    const res = await fetch(apiURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(player)
    })
    return res.json() as Promise<Player>
}

export async function deletePlayer (email: string): Promise<MessageRes> {
    const res = await fetch(apiURL + email, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
    return res.json() as Promise<MessageRes>
}

export async function updatePlayer(player: PlayerBase): Promise<Player> {
    const res = await fetch(apiURL , {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(player)
    })
    return res.json() as Promise<Player>
}
