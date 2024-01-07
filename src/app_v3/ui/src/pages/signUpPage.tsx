import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { Button} from "@mui/material";
import ArticleIcon from '@mui/icons-material/Article';

import { addPlayer } from "../api/players";
import { PlayerBase } from "../types/datatypes";
import SignUpUserForm from "../forms/SignUpUserFrom";
import MessageAlert from "../components/MessageAlert";


const SignUpPage = () => {

    const [errMsg, setErrMsg] = useState("");
    const [addPlayerMsg, setAddPlayerMsg] = useState("");
    const navigation = useNavigate()

    const gotToEvent = () => {
        const path = "../";
        navigation(path);
    }

    const resetScreen =  () => {
        setErrMsg("");
        setAddPlayerMsg("");
    }
    const signUpUser = (player: PlayerBase) => {
        resetScreen();
        addPlayer(player).then((res) => {
            if ("name" in res) {
                setAddPlayerMsg(`Player with name = ${res.name} and email ${res.email} has been created`)
            } else {
                setErrMsg(res.message)
            }
        }).catch(() => {
            setErrMsg("API is currently down, please try again at a different time.")
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
                    <div className="flex justify-center">
                        <h1 className="text-8xl font-bold m-5">Sign up</h1>
                    </div>
                    <SignUpUserForm submitUser={signUpUser}>
                        <MessageAlert isError={errMsg !== ""} msg={errMsg === "" ? addPlayerMsg : errMsg}/>
                    </SignUpUserForm>
                </div>
            </div>
        </div>
    )
}

export default SignUpPage;