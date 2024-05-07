import App from './components/App';
import Scheduling from './components/Scheduling';
import Schedule from './components/Schedule';
import Apply from './components/Apply';

const routes = [
    {
        path: '/',
        element: <App />,
        children: [
            {
                path: '/scheduling',
                element: <Scheduling />
            },
            {
                path: '/schedule',
                element: <Schedule />
            },
            {
                path: '/apply',
                element: <Apply />
            }

        ]
    }
]

export default routes;