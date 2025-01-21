new Vue({
    delimiters: ['[[', ']]'],
    el: '#records',
    data() {
        return {
            patient_records: []
        }
    },
    mounted() {
        this.getPatientRecords()
    },
    computed() { },
    methods: {
        getPrescription(props) {
            const url = '/prescription/' + props.prescription.prescription_id + '/'
            window.location = url
        },
        async getPatientRecords() {
            const url = '/api/get-patient-records/'
            const result = await axios.get(url)
            if (result) {
                this.patient_records = result.data
            }
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