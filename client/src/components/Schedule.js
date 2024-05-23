import React, { useEffect, useState } from "react";
import SessionCard from "./SessionCard";
import "../styles/schedule.css";

function Schedule() {
    const [sessions, setSessions] = useState([]);
    const [tutors, setTutors] = useState([]);
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    const timeSlots = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17];

    const fetchAllSessions = () => {
        fetch("/sessions")
            .then((res) => res.json())
            .then((data) => {
                setSessions(data);
            })
            .catch((error) => console.log("Error fetching sessions:", error));
    };

    useEffect(() => {
        fetchAllSessions();

        fetch("/tutors")
            .then((res) => res.json())
            .then((data) => {
                setTutors(data);
            })
            .catch((error) => console.log("Error fetching tutors:", error));
    }, []);

    const isTutorAvailable = (tutor, day, time) => {
        return tutor.days_scheduled.includes(day) && !sessions.some(session =>
            session.day_scheduled === day && session.time_scheduled === time && session.tutor_id === tutor.id
        );
    };

    return (
        <div className="scrollable-content">
            {daysOfWeek.map(day => (
                <div key={day} className="day-container">
                    <h2>{day}:</h2>
                    <div className="session-cards-group">
                        {timeSlots.map(time => {
                            const dayTimeSessions = sessions.filter(session =>
                                session.day_scheduled === day && session.time_scheduled === time
                            );
                            const availableTutors = tutors.filter(tutor =>
                                isTutorAvailable(tutor, day, time)
                            );
                            return (
                                <React.Fragment key={`${day}-${time}`}>
                                    {dayTimeSessions.map((session, index) => (
                                        <SessionCard
                                            key={`${day}-${time}-${index}`}
                                            session={session}
                                            onSessionChange={fetchAllSessions}
                                        />
                                    ))}
                                    {dayTimeSessions.length >= 0 && availableTutors.length > 0 && (
                                        <SessionCard
                                            key={`${day}-${time}-empty`}
                                            session={{ day_scheduled: day, time_scheduled: time }}
                                            onSessionChange={fetchAllSessions}
                                        />
                                    )}
                                </React.Fragment>
                            );
                        })}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Schedule;
