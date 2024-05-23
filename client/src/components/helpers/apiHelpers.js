export const fetchTutors = () => {
    return fetch(`/tutors`)
        .then((res) => res.json());
};

export const fetchSessions = () => {
    return fetch(`/sessions`)
        .then((res) => res.json());
};
