new Vue({
    delimiters: ['[[', ']]'],
    el: '#patients',
    data() {
        return {
            is_valid: false,
            notes: '',
            finalRemarks: {
                remarks: false,
                instruction: '',
                prescription_id: null
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
                id: null,
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
        this.hideNotification()
    },
    computed() {},
    methods: {
        async addPrescription() {
            const url = '/api/set-prescription/' + String(this.finalRemarks.prescription_id) + '/'

            const data = {
                "notes": this.notes
            }

            const result = await axios.patch(url, data)
            if (result) {
                console.log(result.data)
                window.location = '/prescription/' + String(this.finalRemarks.prescription_id) + '/'
            }

            this.clearFields()

        },
        hideNotification() {
            document.getElementById('notificationPanel').style.display = 'none'
            document.getElementById('innerMessage').innerHTML = ''
        },
        showNotification(message) {
            document.getElementById('notificationPanel').style.display = 'block'
            document.getElementById('innerMessage').innerHTML = message
        },
        clearFields() {
            this.name = ''
            this.middle_name = ''
            this.last_name = ''
            this.birth_date = ''
            this.sex = ''
            this.finalRemarks.remarks = false
            this.finalRemarks.instruction = ''
            this.notes = ''

        },

        calculateAge(dateString) {
            const birthDate = new Date(dateString)
            const currentDate = new Date()
            let age = currentDate.getFullYear() - birthDate.getFullYear()
            const monthDiff = currentDate.getMonth() - birthDate.getMonth()
            if (monthDiff < 0 || (monthDiff === 0 && currentDate.getDate() < birthDate.getDate())) {
                age--
            }
            return age
        },

        autoFill() {
            const selectedPatient = this.list_of_patients.find(
                (patient) => patient.id === this.patientInfo
            )

            if (selectedPatient) {
                const sex = selectedPatient.sex
                const birthDate = selectedPatient.birth_date

                this.sex = sex === 0 ? 'Male' : sex === 1 ? 'Female' : 'Undefined'
                this.predictingData.sex = sex
                this.age = this.calculateAge(birthDate)
                this.predictingData.age = this.age

                this.name = selectedPatient.name
                this.middle_name = selectedPatient.middle_name
                this.last_name = selectedPatient.last_name

                this.predictingData.id = selectedPatient.id

                console.log(this.predictingData.id)
                console.log(this.name)
                console.log(this.middle_name)
                console.log(this.last_name)
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
        checkNullProperties(predictingData) {
            if (predictingData.sex === null) {
                return false;
            } else if (predictingData.age === null) {
                return false;
            } else if (predictingData.cp === null) {
                return false;
            } else if (predictingData.trestbps === null) {
                return false;
            } else if (predictingData.chol === null) {
                return false;
            } else if (predictingData.thalach === null) {
                return false;
            } else if (predictingData.oldpeak === null) {
                return false;
            } else if (predictingData.slope === null) {
                return false;
            } else if (predictingData.ca === null) {
                return false;
            } else if (predictingData.thal === null) {
                return false;
            } else {
                return true; // No null values found
            }
        },
        async getPrediction() {

            this.clearFields()

            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken
            // console.log(this.checkNullProperties(this.predictingData))
            this.is_valid = this.checkNullProperties(this.predictingData)
            if (this.is_valid === true) {
                await axios
                    .post('/api/get-prediction/', this.predictingData)
                    .then((response) => {
                        console.log(response.data)
                        this.finalRemarks.remarks = response.data.remarks
                        this.finalRemarks.instruction = response.data.message
                        this.finalRemarks.prescription_id = response.data.patient_record_id
                    })
                    .catch((error) => {
                        console.log(error)
                    })
            }

            this.predictingData = {
                id: null,
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

            this.patientInfo = null
            this.sex = null
            this.age = null

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