new Vue({
    delimiters: ['[[', ']]'],
    el: '#accounts',
    data() {
        return {
            isModalActive: false,
            accounts: []
        }
    },
    mounted() {
        this.getAccounts()
    },
    methods: {
        async updateAccount(flag, id) {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            data = {
                'id': id,
                'is_active': flag
            }

            await axios
                .patch('/api/create-account/', data)
                .then((response) => {
                    console.log(response)
                })
                .catch((error) => {
                    console.log(error)
                })
            await this.getAccounts()
        },
        async getAccounts() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .get('/api/create-account/')
                .then((response) => {
                    this.accounts = response.data
                    console.log(this.datasets)
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