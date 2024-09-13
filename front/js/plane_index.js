var vm = new Vue({
    el: '#search-form',
    data: {
        profileUrl: '',
        departureCity: '',
        destinationCity: '',
        departureDate: '',
        username: '',
        accessToken:''
    },
    mounted() {
        // 初始化日期选择器
        new Pikaday({
            field: document.getElementById('departure-date'),
            format: 'YYYY-MM-DD',
            onSelect: date => {
                this.departureDate = this.formatDate(date);
            }
        });


    },
    methods: {


        formatDate(date) {
            const year = date.getFullYear();
            const month = ('0' + (date.getMonth() + 1)).slice(-2);
            const day = ('0' + date.getDate()).slice(-2);
            return `${year}-${month}-${day}`;
        },

        search() {
            var formData = new FormData();
            formData.append('departureCity', this.departureCity);
            formData.append('destinationCity', this.destinationCity);
            formData.append('departureDate', this.departureDate);

            axios.post('http://127.0.0.1:8000/plane/search/', formData)
                .then(response => {
                    const searchResults = response.data.data;
                    const departureCity = response.data.departureCity;
                    const destinationCity = response.data.destinationCity;
                    const departureDate = response.data.departureDate;

                    localStorage.setItem('searchResults', JSON.stringify(searchResults));
                    localStorage.setItem('departureCity', departureCity);
                    localStorage.setItem('destinationCity', destinationCity);
                    localStorage.setItem('departureDate', departureDate);

                    // 跳转到指定页面
                    window.location.href = 'http://127.0.0.1:8080/plane_search.html';
                })
                .catch(error => {
                    // 处理错误
                    console.error(error);
                });
        }
    }
});