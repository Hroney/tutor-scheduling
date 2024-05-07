import { Outlet } from "react-router-dom";
import NavBar from "./NavBar";
import { useEffect, useState } from "react";

function App() {


  return (
    <div className="app">
      <header><NavBar /></header>
      <Outlet />
      <footer></footer>
    </div>
  )
}

export default App;
