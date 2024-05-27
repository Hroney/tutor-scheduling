import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import '../styles/applyform.css';
import '../styles/formlabels.css';

const ApplyForm = () => {
    const [statusOk, setStatusOk] = useState(true);
    const [errorMessage, setErrorMessage] = useState('');

    const coursesList = [
        'math_1', 'math_2', 'math_3', 'math_4',
        'science_1', 'science_2', 'science_3', 'science_4',
        'english_1', 'english_2', 'english_3', 'english_4'
    ];

    const daysList = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

    const initialValues = {
        name: '',
        certification: '',
        courses: [],
        daysAvailable: [],
    };

    const validationSchema = Yup.object({
        name: Yup.string()
            .required('Name is required')
            .min(2, 'Name is too short'),
        certification: Yup.number()
            .required('Certification is required')
            .oneOf([1, 2, 3, 4], 'Invalid certification'),
        courses: Yup.array().of(Yup.string().required('Course is required')).min(1, 'Select at least one course'),
        daysAvailable: Yup.array()
            .of(Yup.string().required('Day is required'))
            .min(1, 'Select at least one day'),
    });

    const onSubmit = async (values, { setSubmitting, resetForm }) => {
        try {
            const tutorResponse = await fetch('/tutors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: values.name,
                    certification_level: values.certification
                })
            });
            const tutorData = await tutorResponse.json();
            const tutorId = tutorData.id;

            if (!tutorResponse.ok) {
                setErrorMessage('A tutor with that name already exists');
                setStatusOk(false);
                setTimeout(() => {
                    setStatusOk(true);
                }, 4000);
                return;
            }

            for (const day of values.daysAvailable) {
                await fetch('/scheduled_days', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        day,
                        tutor_id: tutorId
                    })
                });
            }

            for (const course of values.courses) {
                await fetch('/courses', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: course,
                        tutor_id: tutorId
                    })
                });
            }

            setStatusOk(false);
            console.log('All requests completed successfully');
            setErrorMessage('Welcome to the Team!')

            setTimeout(() => {
                setStatusOk(true);
            }, 4000);

            resetForm();
            setSubmitting(false);
        } catch (error) {
            console.error('Error submitting form:', error);
            setSubmitting(false);
        }
    };

    return (
        <>
            {statusOk ? (
                <Formik
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                    onSubmit={onSubmit}
                >
                    {({ isSubmitting }) => (
                        <Form className="form-container">
                            <div className="section">
                                <label htmlFor="name" className="label">Name</label>
                                <Field type="text" id="name" name="name" />
                                <ErrorMessage name="name" component="div" className="error-message" />
                            </div>

                            <div className="section">
                                <label htmlFor="certification" className="label">Certification</label>
                                <Field as="select" id="certification" name="certification">
                                    <option value="">Select</option>
                                    <option value="1">Certification 1</option>
                                    <option value="2">Certification 2</option>
                                    <option value="3">Certification 3</option>
                                    <option value="4">Certification 4</option>
                                </Field>
                                <ErrorMessage name="certification" component="div" className="error-message" />
                            </div>

                            <div className="section">
                                <label className="label">Courses</label>
                                <div className="course-list">
                                    {coursesList.map(course => (
                                        <div key={course} className="checkbox-container">
                                            <Field type="checkbox" id={course} name="courses" value={course} />
                                            <label htmlFor={course} className="checkbox-label">{course}</label>
                                        </div>
                                    ))}
                                </div>
                                <ErrorMessage name="courses" component="div" className="error-message" />
                            </div>

                            <div className="section">
                                <label className="label">Days Available</label>
                                <div className="day-list">
                                    {daysList.map(day => (
                                        <div key={day} className="checkbox-container">
                                            <Field type="checkbox" id={day} name="daysAvailable" value={day} />
                                            <label htmlFor={day} className="checkbox-label">{day}</label>
                                        </div>
                                    ))}
                                </div>
                                <ErrorMessage name="daysAvailable" component="div" className="error-message" />
                            </div>


                            <button type="submit" disabled={isSubmitting}>
                                Submit
                            </button>
                        </Form>
                    )}
                </Formik>
            ) : (
                <div className={errorMessage == 'Welcome to the Team!' ? "welcome-message" : "error-message"}>
                    {errorMessage}
                </div>
            )}
        </>
    );
}

export default ApplyForm;
