import "./App.css"
import AdminPage from "./pages/AdminPage";
import EventsPage from "./pages/EventsPage";
import SignUpPage from "./pages/SignUpPage";
import EventPage from "./pages/EventPage";
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
