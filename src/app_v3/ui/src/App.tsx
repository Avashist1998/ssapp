import "./App.css"
import AdminPage from "./pages/adminPage";
import EventsPage from "./pages/eventsPage";
import SignUpPage from "./pages/signUpPage";
import EventPage from "./pages/eventPage";
import { BrowserRouter, Route, Routes } from "react-router-dom"




function App() {
  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/admin" Component={AdminPage}/>
        <Route path="/signUp" Component={SignUpPage}/>
        <Route path="/events" Component={EventsPage}/>
        <Route path="/events/:eventId" Component={EventPage}/>
      </Routes>
    </BrowserRouter>

      
    </>
  )
}

export default App
