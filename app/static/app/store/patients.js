new Vue({
    delimiters: ['[[', ']]'],
    el: '#patients',
    data() {
        return {
            message: 'Testing',
            name: null,
            middle_name: null,
            last_name: null,
            birth_date: null,
        }
    },
    mounted() {},
    methods: {
        clearFields() {
            this.name = ''
            this.middle_name = ''
            this.last_name = ''
            this.birth_date = ''
        },
        async addPatients() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .post('/api/add-patients', {
                    name: this.name,
                    middle_name: this.middle_name,
                    last_name: this.last_name,
                    birth_date: this.birth_date
                })
                .then((response) => {
                    this.reports = response.data
                    console.log(this.reports)
                })
                .catch((error) => {
                    console.log(error)
                })
        },
        getCookie(name) {
            const cookieValue = document.cookie
                .split(';')
                .map((cookie) => cookie.trim())
                .find((cookie) => cookie.startsWith(name + '='))

            if (cookieValue) {
                return decodeURIComponent(cookieValue.split('=')[1])
            } else {
                return null
            }
        },
    },
})