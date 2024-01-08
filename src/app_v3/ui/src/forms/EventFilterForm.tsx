import { useState } from "react";

import { Button, FormControl, InputLabel, MenuItem, Select, TextField, Box } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";



const EventFilterForm = (props: {
    onSubmit: (searchText: string, type: string) => void,
}) => {
    const [type, setType] = useState("Both");
    const [searchText, setSearchText] = useState("");


    const onSubmit = () => {
        props.onSubmit(searchText, type);
    }
    return (
        <div className="flex justify-center items-center my-2">
            <TextField  id="searchText" variant="standard" value={searchText} onChange={e => {
                setSearchText(e.target.value);
            }} />
            <div className="mx-5">
                <Box sx={{ minWidth: 120 }}>
                    <FormControl fullWidth>
                        <InputLabel id="type-select-label">Type</InputLabel>
                        <Select
                            labelId="type-select-label"
                            id="type-select"
                            value={type}
                            label="Age"
                            onChange={(e) => {setType(e.target.value as string)}}
                        >
                            <MenuItem value={"Both"}>Both</MenuItem>
                            <MenuItem value={"Private"}>Private</MenuItem>
                            <MenuItem value={"Public"}>Public</MenuItem>
                        </Select>
                    </FormControl>
                </Box>
            </div>
            <div className="mx-5">
                <Button onClick={onSubmit} startIcon={<SearchIcon/>} variant="contained" color="success">
                    Submit
                </Button>
            </div>
        </div>
    )
}


export default EventFilterForm;