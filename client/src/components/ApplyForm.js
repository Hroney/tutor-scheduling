import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const ApplyForm = () => {
    const [tutors, setTutors] = useState([{}]);
    const [refreshPage, setRefreshPage] = useState(false);



    return (
        <div>
            <h1>Apply</h1>
            <Formik
                initialValues={{
                    name: '',
                    email: '',
                    message: ''
                }}
                validationSchema={Yup.object({
                    name: Yup.string()
                        .required('Required'),
                    email: Yup.string()
                        .email('Invalid email address')
                        .required('Required'),
                    message: Yup.string()
                        .required('Required')
                })}
                onSubmit={(values, { setSubmitting }) => {
                    setTimeout(() => {
                        alert(JSON.stringify(values, null, 2));
                        setSubmitting(false);
                    }, 400);
                }}
            >
                <Form>
                    <div>
                        <label htmlFor="name">Name</label>
                        <Field type="text" name="name" />
                        <ErrorMessage name="name" />
                    </div>
                    <div>
                        <label htmlFor="email">Email Address</label>
                        <Field type="email" name="email" />
                        <ErrorMessage name="email" />
                    </div>
                    <div>
                        <label htmlFor="message">Message</label>
                        <Field as="textarea" name="message" />
                        <ErrorMessage name="message" />
                    </div>
                    <button type="submit">Submit</button>
                </Form>
            </Formik>
        </div>
    );
}

export default ApplyForm;