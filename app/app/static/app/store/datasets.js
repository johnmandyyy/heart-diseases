new Vue({
    delimiters: ['[[', ']]'],
    el: '#datasets',
    data() {
        return {
            datasets: [],
            testing: [],
            is_training_done: true,
            isModalActive: false,
            cardio_info: {
                "first_name": "",
                "last_name": "",
                "suffixes": "",
                "license_no": "",
                "e_signature": ""
            },
            modalContent: {
                title: null,
                message: null
            },
            fileName: ''
        }
    },
    mounted() {
        this.getDatasets()
        this.getTesting()
        this.getCardioInfo()
    },
    methods: {
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileName = file; // Update the fileName with the name of the selected file
            } else {
                this.fileName = ''; // Reset if no file is selected
            }
        },
        async updateCardioInfo() {
            try {
                const formData = new FormData();

                // Append all the other fields that need to be updated
                formData.append('suffixes', this.cardio_info.suffixes);
                formData.append('license_no', this.cardio_info.license_no);

                // If a new file (e_signature) is selected, append it
                if (this.fileName) {
                    formData.append('e_signature', this.fileName);
                }

                // Set the CSRF token for the request headers
                const csrftoken = this.getCookie('csrftoken');
                axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

                // Send the data using PATCH (or POST) request to update the cardiologist info
                const response = await axios.patch('/api/get-cardiologists/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data', // Important for file uploads
                    },
                });
                console.log('Cardiologist info updated:', response.data);
            } catch (error) {
                console.error('Error updating cardiologist info:', error);
            }

            await this.getCardioInfo()
        },
        async getCardioInfo() {
            const csrftoken = this.getCookie('csrftoken')
            axios.defaults.headers.common['X-CSRFToken'] = csrftoken
            await axios
                .get('/api/get-cardiologists/')
                .then((response) => {
                    console.log(response.data)
                    this.cardio_info = {
                        "first_name": response.data.first_name,
                        "last_name": response.data.last_name,
                        "suffixes": response.data.suffixes,
                        "license_no": response.data.license_no,
                        "e_signature": response.data.e_signature
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
        },
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