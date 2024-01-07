import {List, ListItem, ListItemText} from '@mui/material'

import { Entry } from '../types/datatypes'


const EntriesList = ( props : {
    entries: Entry[],
    children?: React.ReactNode
}) => {

    return (
        <>
            {props.children}
            <div className="flex justify-center">
                <h1  className="text-2xl font-bold">Players</h1>
            </div>
            <div className="flex justify-center">
                <List>
                    {props.entries.map((entry) => {
                    return (
                        <ListItem key={entry.id}>
                            <ListItemText primary={entry.player_email} secondary= {new Date(entry.created_date).toLocaleDateString()}/>
                        </ListItem>
                        )
                    })
                }
                </List>
            </div>
        </>

    )
}

export default EntriesList;