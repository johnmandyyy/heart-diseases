new Vue({
    delimiters: ['[[', ']]'],
    el: '#accounts',
    data() {
        return {
            isModalActive: false,
            datasets: [],
            testing: []
        }
    },
    mounted() {
        this.getDatasets()
        this.getTesting()
    },
    methods: {
        async getDatasets() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .get('/api/get-datasets-heart/')
                .then((response) => {
                    this.datasets = response.data
                    console.log(this.datasets)
                })
                .catch((error) => {
                    console.log(error)
                })
        },
        async getTesting() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .get('/api/get-testing/')
                .then((response) => {
                    this.testing = response.data
                    console.log(this.testing)
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