import { Formik, Form, Field } from "formik";
import { useState } from "react";
// import '../styles/signupform.css';

const SignUpForm = ({ session, handleClose }) => {
    const [showSuccess, setShowSuccess] = useState(false);

    const handleSubmit = (values, { setSubmitting }) => {
        console.log(values)

        setTimeout(() => {
            setShowSuccess(true);
            setSubmitting(false);
            setTimeout(() => {
                handleClose();
            }, 1500);
        }, 1000);
    };

    return (
        <div className="signup-form-container">
            <h2>Sign Up for Session</h2>
            <Formik
                initialValues={{ name: "" }}
                onSubmit={handleSubmit}
            >
                {({ isSubmitting }) => (
                    <Form>
                        <Field type="text" name="name" placeholder="Your Name" />
                        {!showSuccess ?
                            <button type="submit" disabled={isSubmitting}>
                                {isSubmitting ? "Submitting..." : "Submit"}
                            </button> : null
                        }

                    </Form>
                )}
            </Formik>
            {showSuccess && <p className="success-message">Sign-up successful!</p>}
        </div>
    );
};

export default SignUpForm;
