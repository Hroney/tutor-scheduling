import { NavLink } from 'react-router-dom';
import '../styles/navbar.css'

function NavBar() {

    return (
        <nav className="nav-bar">
            <NavLink
                to="/scheduling"
                className="nav-link"
            >
                Sign up
            </NavLink>
            <NavLink
                to="/schedule"
                className="nav-link"
            >
                Schedule
            </NavLink>
            <NavLink
                to="/apply"
                className="nav-link"
            >
                Apply to be a Tutor
            </NavLink>
        </nav>
    )
}

export default NavBar