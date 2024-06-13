import React, { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
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
        let tutee = {
            name: values.name,
            student_number: values.student_id,
        };

        fetch(`/tutees/${values.student_id}/student_number`)
            .then((res) => {
                if (!res.ok) {
                    return fetch('/tutees', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(tutee)
                    })
                        .then(postResponse => {
                            if (!postResponse.ok) {
                                throw new Error('Failed to post tutee');
                            }
                            return postResponse.json();
                        });
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
                };
                return fetch("/sessions", {
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
                });
            })
            .catch((error) => console.error('There was a problem with the fetch operation:', error));

        setTimeout(() => {
            setShowSuccess(true);
            setSubmitting(false);
            setTimeout(handleClose, 1500);
        }, 1000);
    };


    const validationSchema = Yup.object().shape({
        name: Yup.string()
            .min(2, 'Name must be at least 2 characters long')
            .required('Name is required'),
        student_id: Yup.string()
            .matches(/^4000\d{6}$/, 'Student number must be 10 digits and start with 4000')
            .required('Student number is required')
    });

    return (
        <div className="signup-form-container">
            <h2>Sign Up for Session</h2>
            <Formik
                initialValues={{ name: '', student_id: '', tutor: '', course: '' }}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting, setFieldValue, values, errors, touched }) => (
                    <Form>
                        <div>
                            <Field type="text" name="name" placeholder="Your Name" />
                            {errors.name && touched.name ? (
                                <div className="error-message">{errors.name}</div>
                            ) : null}
                        </div>
                        <div>
                            <Field type="text" name="student_id" placeholder="Your ID number" />
                            {errors.student_id && touched.student_id ? (
                                <div className="error-message">{errors.student_id}</div>
                            ) : null}
                        </div>
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
