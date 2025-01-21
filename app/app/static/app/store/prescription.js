new Vue({
    delimiters: ['[[', ']]'],
    el: '#prescription',
    data() {
        return {}
    },
    mounted() {

    },
    methods: {
        automatePrint() {
            console.log('printing')
            window.print()
        }
    },
})