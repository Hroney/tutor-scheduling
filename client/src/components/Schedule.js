import { useEffect, useState } from "react";
import SessionCard from "./SessionCard";
import "../styles/schedule.css"

function Schedule() {
    const [sessions, setSessions] = useState([]);
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    const timeSlots = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17];

    useEffect(() => {
        fetch("/sessions")
            .then((res) => res.json())
            .then((data) => {
                setSessions(data);
            })
            .catch((error) => console.log("Error fetching sessions:", error));
    }, []);

    return (
        <div className="scrollable-content">
            {daysOfWeek.map(day => (
                <div key={day} className="day-container">
                    <h2>{day}:</h2>
                    <div className="session-cards-group">
                        {timeSlots.map(time => {
                            const session = sessions.find(session =>
                                session.day_scheduled === day && session.time_scheduled === time
                            );
                            return (
                                <SessionCard
                                    key={`${day}-${time}`}
                                    session={session || { day_scheduled: day, time_scheduled: time }}
                                />
                            );
                        })}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Schedule;
