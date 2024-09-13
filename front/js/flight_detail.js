new Vue({
    el: '#app',
    data: {

        flightDetail: null,
        imageUrl:'',
                passengerName: '',
        passengerGender: '',  // 添加此属性
        passengerPhone: '',   // 添加此属性
        passengerId: ''       // 添加此属性



    },
    mounted() {


        // 获取 URL 参数并请求航班详情
        const urlParams = new URLSearchParams(window.location.search);
        const flightId = urlParams.get('id');
        if (flightId) {
            this.fetchFlightDetails(flightId);
        }
    },
    methods: {
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) {
                const cookieValue = parts.pop().split(';').shift();
                return cookieValue.trim(); // 返回去除空格后的 cookie 值
            }
        },
        logoutfunc() {
            console.log('Logout function called');

            var url = 'http://127.0.0.1:8000/user/logout/';
            axios.delete(url, {
                withCredentials: true,
            })
            .then(response => {
                location.href = 'http://127.0.0.1:8080/login.html';
            })
            .catch(error => {
                console.log(error.response);
            });
        },
        fetchFlightDetails(id) {
            axios.get(`http://127.0.0.1:8000/plane/flight_detail/${id}/`, {
                withCredentials: true,
                headers: {
                    'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部
                }
            })
            .then(response => {
                // 将获取到的航班详情赋值给 flightDetail
                this.flightDetail = response.data;
                 // 基本 URL
                const baseUrl = "http://127.0.0.1:8080/";
                this.imageUrl = baseUrl + this.flightDetail.logo;


                console.log('Flight Details:', this.flightDetail);
            })
            .catch(error => {
                console.log('Error fetching flight details:', error.response);
            });
        },

        submitForm() {
    var name = document.getElementById('passengerName').value;
    var gender = document.getElementById('passengerGender').value;
    var phone = document.getElementById('passengerPhone').value;
    var credit = document.getElementById('passengerId').value;
    if (!this.flightDetail || !this.flightDetail.id) {
        console.error('Flight details are not available.');
        return;
    }

    // 创建要发送的数据对象
    var data = {
        name: name,
        gender: gender,
        phone: phone,
        credit: credit,
        flight_id: this.flightDetail.id
    };


    // 发送 POST 请求
    axios.post('http://127.0.0.1:8000/plane/flight_order/', data, {
        withCredentials: true,  // 允许携带 cookies
        headers: {
            'Content-Type': 'application/json',
           'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部

        }
    })
    .then(response => {
        console.log('服务器响应:', response.data);
    })
    .catch(error => {
        console.error('错误:', error);
    });
}
    }
});