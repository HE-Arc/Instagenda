import './assets/main.css'

import { createApp } from 'vue'
import { Quasar } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const getCSRFToken = () => {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

const updateCSRF = () => {
    const csrfToken = getCSRFToken();
    if (csrfToken) {
        axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
    }
};

axios.defaults.baseURL = import.meta.env.VITE_API_URL
axios.defaults.withCredentials = true
updateCSRF();

const app = createApp(App)

app
.use(Quasar, {
    plugins: {},
    config: {
        dark: window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches,
    },
})
.use(router)

app.mount('#app')

export { updateCSRF }