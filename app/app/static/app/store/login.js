new Vue({
    delimiters: ['[[', ']]'],
    el: '#sample-modal',
    data() {
        return {
            'first_name': null,
            'last_name': null,
            'email_address': null,
            'username': null,
            'password': null,
            'is_staff': 0
        }
    },
    mounted() {
        this.defaultMethod()
    },
    methods: {
        defaultMethod() {
            console.log('executed')
        },
        async createAccount() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken
            console.log(this.is_staff)
            console.log(typeof(this.is_staff))

            if (this.is_staff === 0) {
                this.is_staff = true
            } else {
                this.is_staff = false
            }

            data = {
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email_address,
                'username': this.username,
                'password': this.password,
                'is_staff': this.is_staff
            }
            console.log(data)
            await axios
                .post('/api/create-account/', data)
                .then((response) => {
                    console.log(response.data)
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