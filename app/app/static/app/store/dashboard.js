new Vue({
    delimiters: ['[[', ']]'],
    el: '#dashboard',
    data() {
        return {
            reports: [],
        }
    },
    mounted() {
        this.getReports()
    },
    methods: {
        async getReports() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .get('/api/get-reports')
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