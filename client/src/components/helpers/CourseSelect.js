import React from 'react';
import { Field } from 'formik';

const CourseSelect = ({ courses, value }) => (
    <Field as="select" name="course" value={value}>
        <option value="">Select Course</option>
        {courses.map(course => (
            <option key={course} value={course}>
                {course}
            </option>
        ))}
    </Field>
);

export default CourseSelect;
