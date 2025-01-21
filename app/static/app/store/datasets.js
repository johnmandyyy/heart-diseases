new Vue({
    delimiters: ['[[', ']]'],
    el: '#datasets',
    data() {
        return {
            datasets: [],
            testing: [],
            is_training_done: true,
            isModalActive: false,
            modalContent: {
                title: null,
                message: null
            }
        }
    },
    mounted() {
        this.getDatasets()
        this.getTesting()
    },
    methods: {
        async trainDataSet() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken
            this.is_training_done = false
            await axios
                .post('/api/train-heart-dataset/', {
                    is_train: true
                })
                .then((response) => {
                    console.log(response.data)
                    this.modalContent.title = 'Notification:'
                    this.modalContent.message = response.data.message
                    this.isModalActive = true

                    setTimeout(() => {
                        this.modalContent.title = ''
                        this.modalContent.message = ''
                        this.isModalActive = false

                    }, 5000) // 3000 milliseconds = 3 seconds
                })
                .catch((error) => {
                    console.log(error)
                })
            this.is_training_done = true
        },
        getDatasets() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            axios
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