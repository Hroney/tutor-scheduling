import React, { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import { fetchTutors, fetchSessions } from './helpers/apiHelpers';
import { filterAvailableTutors, handleTutorChange } from './helpers/formHelpers';
import TutorSelect from './helpers/TutorSelect';
import CourseSelect from './helpers/CourseSelect';

const SignUpForm = ({ session, handleClose, onSessionChange }) => {
    const [showSuccess, setShowSuccess] = useState(false);
    const [tutors, setTutors] = useState([]);
    const [filteredTutors, setFilteredTutors] = useState([]);
    const [selectedTutorCourses, setSelectedTutorCourses] = useState([]);
    const [sessions, setSessions] = useState([]);
    const [reload, setReload] = useState(false);

    useEffect(() => {
        fetchTutors().then(setTutors).catch(console.error);
        fetchSessions().then(setSessions).catch(console.error);
    }, [reload]);

    useEffect(() => {
        setFilteredTutors(filterAvailableTutors(tutors, sessions, session));
    }, [tutors, sessions, session.day_scheduled, session.time_scheduled, session]);

    const handleSubmit = (values, { setSubmitting }) => {
        console.log("Values:", values);
        console.log("Session:", session);

        let tutee = {
            name: values.name,
            student_number: values.student_id,
        }

        fetch(`tutees/${values.student_id}/student_number`)
            .then((res) => {
                if (!res.ok) {
                    return fetch('tutees', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(tutee)
                    })
                        .then(postResponse => {
                            if (!postResponse.ok) {
                                throw new Error('failed to post tutee');
                            }
                            return postResponse.json();
                        })
                }
                return res.json();
            })
            .then((data) => {
                let returnobj = {
                    course: values.course,
                    time_scheduled: session.time_scheduled,
                    day_scheduled: session.day_scheduled,
                    tutor_id: parseInt(values.tutor),
                    tutee_id: parseInt(data.id)
                }
                fetch("sessions", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(returnobj, null, 2)
                }).then((res) => {
                    if (res.status !== 201) {
                        console.log("fail", res);
                    } else {
                        console.log("pass", res);
                        setReload(!reload);
                        onSessionChange();
                    }
                })
            })
            .catch((error) => console.error('There was a problem with the fetch operation:', error));

        setTimeout(() => {
            setShowSuccess(true);
            setSubmitting(false);
            setTimeout(handleClose, 1500);
        }, 1000);
    };

    return (
        <div className="signup-form-container">
            <h2>Sign Up for Session</h2>
            <Formik
                initialValues={{ name: '', student_id: '', tutor: '', course: '' }}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting, setFieldValue, values }) => (
                    <Form>
                        <Field type="text" name="name" placeholder="Your Name" />
                        <Field type="text" name="student_id" placeholder="Your ID number" />
                        <TutorSelect
                            tutors={filteredTutors}
                            value={values.tutor}
                            onChange={e => handleTutorChange(e, setFieldValue, filteredTutors, setSelectedTutorCourses)}
                        />

                        <CourseSelect
                            courses={selectedTutorCourses}
                            value={values.course}
                        />

                        {!showSuccess && (
                            <button type="submit" disabled={isSubmitting}>
                                {isSubmitting ? 'Submitting...' : 'Submit'}
                            </button>
                        )}
                    </Form>
                )}
            </Formik>
            {showSuccess && <p className="success-message">Sign-up successful!</p>}
        </div>
    );
};

export default SignUpForm;
