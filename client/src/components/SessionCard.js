import '../styles/sessioncard.css'


const SessionCard = ({ session }) => {
  let time = session.time_scheduled;
  let ampm = time >= 12 ? " pm" : " am";

  return (
    <div className="session-card">
      <h2>{session.course}</h2>
      <p><strong>Time:</strong> {session.time_scheduled >= 13 ? (time - 12) + ampm : time + ampm}</p>
      {/* Add more session details here */}
    </div>
  );
};

export default SessionCard