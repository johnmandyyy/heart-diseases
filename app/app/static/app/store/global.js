new Vue({
    delimiters: ['[[', ']]'],
    el: '#global',
    data() {
        return {
            notificationVisible: true,
            globalMessage: 'Hello'
        }
    },
    mounted() { },
    methods: {
        globalAlert() {
            alert('Global Alert!')
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