import React from 'react';
import { Field } from 'formik';

const TutorSelect = ({ tutors, value, onChange }) => (
    <Field as="select" name="tutor" value={value} onChange={onChange}>
        <option value="">Select Tutor</option>
        {tutors.map(({ id, name }) => (
            <option key={id} value={id}>
                {name}
            </option>
        ))}
    </Field>
);

export default TutorSelect;
