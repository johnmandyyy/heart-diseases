new Vue({
    delimiters: ['[[', ']]'],
    el: '#patients',
    data() {
        return {
            finalRemarks: {
                remarks: false,
                instruction: ''
            },
            name: null,
            middle_name: null,
            last_name: null,
            birth_date: null,
            sex: null,
            age: 0,
            list_of_patients: [],
            patientInfo: '',
            predictingData: {
                sex: null,
                age: null,
                cp: null,
                trestbps: null,
                chol: null,
                fbs: false,
                thalach: null,
                exang: false,
                oldpeak: null,
                slope: null,
                ca: null,
                thal: null,
            },
        }
    },
    mounted() {
        this.getPatients()
    },
    computed() {},
    methods: {
        clearFields() {
            this.name = ''
            this.middle_name = ''
            this.last_name = ''
            this.birth_date = ''
            this.sex = ''

            this.finalRemarks.remarks = false
            this.finalRemarks.instruction = ''

        },

        calculateAge(dateString) {
            // Convert the date string into a JavaScript Date object
            const birthDate = new Date(dateString)

            // Get the current date
            const currentDate = new Date()

            // Calculate the difference between the current date and the birth date
            let age = currentDate.getFullYear() - birthDate.getFullYear()

            // Check if the current date is before the birthday of the current year
            const monthDiff = currentDate.getMonth() - birthDate.getMonth()
            if (
                monthDiff < 0 ||
                (monthDiff === 0 && currentDate.getDate() < birthDate.getDate())
            ) {
                age--
            }
            return age
        },

        autoFill() {
            // Get the selected patient object from the list_of_patients
            const selectedPatient = this.list_of_patients.find(
                (patient) => patient.id === this.patientInfo
            )

            console.log(selectedPatient)
            // Check if a patient with the selected ID exists
            if (selectedPatient) {
                // Access the sex and birth_date properties of the selected patient
                const sex = selectedPatient.sex
                const birthDate = selectedPatient.birth_date

                this.sex = sex === 1 ? 'Male' : sex === 2 ? 'Female' : 'Undefined'
                this.predictingData.sex = sex
                this.age = this.calculateAge(birthDate)
                this.predictingData.age = this.age

                this.name = selectedPatient.name
                this.middle_name = selectedPatient.middle_name
                this.last_name = selectedPatient.last_name

                console.log(this.name)
                console.log(this.middle_name)
                console.log(this.last_name)

                // Print the sex and birth date to the console or do whatever you need with them
                console.log('Sex:', sex)
                console.log('Birth Date:', this.age)
            } else {
                console.log('Patient not found')
            }
        },

        async getPatients() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .get('/api/add-patients/')
                .then((response) => {
                    console.log(response)
                    this.list_of_patients = response.data
                })
                .catch((error) => {
                    console.log(error)
                })
        },
        async getPrediction() {
            this.clearFields()


            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .post('/api/get-prediction/', this.predictingData)
                .then((response) => {
                    console.log(response.data)
                    this.finalRemarks.remarks = response.data.remarks
                    this.finalRemarks.instruction = response.data.message
                    console.log(this.finalRemarks)
                })
                .catch((error) => {
                    console.log(error)
                })

            this.predictingData = {
                sex: null,
                age: null,
                cp: null,
                trestbps: null,
                chol: null,
                fbs: false,
                thalach: null,
                exang: false,
                oldpeak: null,
                slope: null,
                ca: null,
                thal: null,
            }
        },
        async addPatients() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken

            await axios
                .post('/api/add-patients/', {
                    name: this.name,
                    middle_name: this.middle_name,
                    last_name: this.last_name,
                    birth_date: this.birth_date,
                    sex: this.sex,
                })
                .then((response) => {
                    console.log(response)
                })
                .catch((error) => {
                    console.log(error)
                })

            this.getPatients()
            this.clearFields()
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