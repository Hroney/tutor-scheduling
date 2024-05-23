export const filterAvailableTutors = (tutors, sessions, session) => {
    return tutors.filter(tutor =>
        tutor.days_scheduled.includes(session.day_scheduled) &&
        !sessions.some(s =>
            s.tutor_id === tutor.id &&
            s.day_scheduled === session.day_scheduled &&
            s.time_scheduled === session.time_scheduled
        )
    );
};

export const handleTutorChange = (event, setFieldValue, filteredTutors, setSelectedTutorCourses) => {
    const tutorId = event.target.value;
    const tutor = filteredTutors.find(t => t.id === parseInt(tutorId, 10));

    if (tutor) {
        setSelectedTutorCourses(tutor.courses);
        setFieldValue('tutor', tutorId);
        setFieldValue('course', '');
    } else {
        setSelectedTutorCourses([]);
        setFieldValue('tutor', '');
        setFieldValue('course', '');
    }
};
