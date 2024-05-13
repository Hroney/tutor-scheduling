import { useState, useEffect } from "react";
import SignUpForm from "./SignUpForm";
import '../styles/sessioncard.css';

const SessionCard = ({ session }) => {
  const [tutor, setTutor] = useState(null);
  const [tutee, setTutee] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [timer, setTimer] = useState(false);
  const [showSignUpForm, setShowSignUpForm] = useState(false);

  let time = session.time_scheduled;
  let ampm = time >= 12 ? " pm" : " am";

  useEffect(() => {
    const timeOut = setTimeout(() => {
      setTimer(expanded);
    }, 300);

    return () => clearTimeout(timeOut);
  }, [expanded]);

  useEffect(() => {
    if (timer) {
      fetch(`/tutors/${session.tutor_id}`)
        .then((res) => res.json())
        .then((data) => setTutor(data))
        .catch((error) => console.log("Error fetching tutor:", error));

      fetch(`/tutees/${session.tutee_id}`)
        .then((res) => res.json())
        .then((data) => setTutee(data))
        .catch((error) => console.log("Error fetching tutee:", error));
    }
  }, [timer, session.tutor_id, session.tutee_id]);

  const handleButtonClick = () => {
    setShowSignUpForm(true);
  };

  const handleCloseSignUpForm = () => {
    setShowSignUpForm(false);
  };

  if (session.course) {
    return (
      <div className={`session-card ${expanded ? 'expanded' : ''}`} onClick={() => setExpanded(!expanded)}>
        <h2>{session.course}</h2>
        <p><strong>Time:</strong> {session.time_scheduled >= 13 ? (time - 12) + ampm : time + ampm}</p>
        {timer && tutor && tutee && (
          <div className="additional-info">
            <p><strong>Tutor:</strong> {tutor.name}</p>
            <p><strong>Tutee:</strong> {tutee.name}</p>
          </div>
        )}

      </div>
    );
  } else {
    return (
      <div className={`session-card ${expanded ? 'expanded' : ''}`}>
        <button onClick={showSignUpForm ? handleCloseSignUpForm : handleButtonClick}><strong>{showSignUpForm ? "Cancel" : "Sign up"}</strong></button>
        <p><strong>Time:</strong> {session.time_scheduled >= 13 ? (time - 12) + ampm : time + ampm}</p>
        {showSignUpForm && <SignUpForm session={session} handleClose={handleCloseSignUpForm} />}
      </div>
    )
  }
};

export default SessionCard;
