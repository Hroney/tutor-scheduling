import { useEffect, useState } from "react";
import SessionCard from "./SessionCard"
import '../styles/sessioncard.css'

function Schedule() {
    const [sessions, setSessions] = useState([])
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

    useEffect(() => {
        fetch("/sessions")
            .then((res) => res.json())
            .then((data) => {
                setSessions(data)
            })
    }, 0)

    return (
        <div className="scrollable-content">
            {daysOfWeek.map(day => (
                <div key={day} className="day-container">
                    <h2>{day}:</h2>
                    <div className="session-cards-group">
                        {sessions
                            .filter(session => session.day_scheduled === day)
                            .sort((a, b) => a.time_scheduled - b.time_scheduled)
                            .map(session => (
                                <SessionCard key={session.id} session={session} />
                            ))}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Schedule;