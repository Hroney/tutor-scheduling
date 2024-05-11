import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";
import { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import '../styles/main.css'

function App() {


  return (
    <div className="App">
      <header><NavBar /></header>
      <main className="content">
        <Outlet />
        <aside>
          <Sidebar />
        </aside>
      </main>
      <footer>"This is</footer>
    </div>
  )
}

export default App;
