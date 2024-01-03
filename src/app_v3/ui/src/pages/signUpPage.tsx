import { useEffect, useState } from "react";
import { TextField, Button, InputLabel } from "@mui/material";
import { useNavigate } from "react-router-dom";

import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import ArticleIcon from '@mui/icons-material/Article';

import { addPlayer } from "../api/players";
import { PlayerBase } from "../types/datatypes";

const SignUpPage = () => {
    const [userName, setUserName] = useState("");
    const [userEmail, setUserEmail] = useState("");
    const [enableSignUpButton, setEnableSignUpButton] = useState(false);
    const navigation = useNavigate()


    const gotToEvent = () => {
        const path = "../events";
        navigation(path);
    }

    useEffect(() => {
        let val = true;
        if (userName === "") {
            val = val && false;
        }
        if (userEmail === "") {
            val = val && false;
        }
        if (!userEmail.includes("@")) {
            val = val && false;
        }
        setEnableSignUpButton(val);
    }, [userName, userEmail])

    const signUpUser = () => {
        const player = {
            name: userName,
            email: userEmail
        } as PlayerBase;
        addPlayer(player).then((res) => {
            console.log(res);
            setUserName("");
            setUserEmail("");
        })
    }
    return (
        <div className="p-[20px]">
            <div className="flex justify-end left-0">
                <Button startIcon={<ArticleIcon/>} variant="contained" color="primary" onClick={gotToEvent}>
                    Events
                </Button>
            </div>
            <div className="justify-center flex">
                <div>
                    <h1 className="text-8xl font-bold m-5">Sign up</h1>
                    <div>
                        <div className="justify-center flex p-2">
                            <InputLabel>User Name:</InputLabel>
                            <TextField id="eventName" label="Required" value={userName} required onChange={e => setUserName(e.target.value)}/>
                        </div>
                        <div className="justify-center flex p-2">
                            <InputLabel>User Email: </InputLabel>
                            <TextField id="creatorEmail" label="Required" value={userEmail} required onChange={e => setUserEmail(e.target.value)}/>
                        </div>
                    </div>
                    <div className="justify-center flex">
                        <Button startIcon={<PersonAddAltIcon/>} variant="contained" color="success" disabled={!enableSignUpButton} onClick={signUpUser}>
                            Sign Up
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignUpPage;