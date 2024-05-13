import { Outlet, useLocation } from "react-router-dom";
import NavBar from "./NavBar";
import { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import '../styles/main.css';

function App() {
  const location = useLocation();
  const isBaseRoute = location.pathname === '/';

  return (
    <div className="App">
      <header><NavBar /></header>
      <main className="content">
        <Outlet />
        {isBaseRoute ? null : (
          <aside>
            <Sidebar />
          </aside>
        )}
      </main>
      <footer>"This is a footer"</footer>
    </div>
  )
}

export default App;
