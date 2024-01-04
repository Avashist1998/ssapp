import "./App.css"
import AdminPage from "./pages/adminPage";
import EventsPage from "./pages/eventsPage";
import SignUpPage from "./pages/signUpPage";
import EventPage from "./pages/eventPage";
import { Route, Routes, HashRouter } from "react-router-dom"




function App() {
  return (
    <>
    <HashRouter>
      <Routes>
        <Route path="/admin" Component={AdminPage}/>
        <Route path="/signUp" Component={SignUpPage}/>
        <Route path="" Component={EventsPage}/>
        <Route path="/:eventId" Component={EventPage}/>
      </Routes>
    </HashRouter>

      
    </>
  )
}

export default App
