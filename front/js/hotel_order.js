const selectedRoomId = JSON.parse(localStorage.getItem('selectedRoomId'));

new Vue({
    el: '#app',
    data: {
        username:'',
        selectedRoomId: selectedRoomId,
        room: {},
        hotel: {},
        estimatedArrivalOptions: [],
        checkInDate: null,
        checkOutDate: null,
        totalPrice: null,
        roomCount: 1 ,
        guestName: '',
        email: '',
        phoneNumber: '',
        estimatedArrivalTime: ''

    },
    computed: {
        formattedCheckInDate() {
            if (!this.checkInDate) return '';
            return this.formatDate(this.checkInDate);
        },
        formattedCheckOutDate() {
            if (!this.checkOutDate) return '';
            return this.formatDate(this.checkOutDate);
        }
    },
    mounted() {

         axios.interceptors.response.use(
        response => {
            return response;
        },
        error => {
            if (error.response && error.response.status === 401) {
    if (confirm('请先进行登录')) {
        window.location.href = 'http://127.0.0.1:8080/login.html';
    }
}else {
                return Promise.reject(error);
            }
        }
    );
        this.sendSelectedRoomIdToBackend();

        this.initializeDatePickers();
        this.initializeEstimatedArrivalTimeSelect();
    },
    watch: {
        checkInDate(newCheckInDate) {
            this.calculateTotalPrice();
        },
        checkOutDate(newCheckOutDate) {
            this.calculateTotalPrice();
        },
        roomCount(newRoomCount) {
            this.calculateTotalPrice();
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

        calculateTotalPrice() {
            if (this.checkInDate && this.checkOutDate) {
                const oneDay = 24 * 60 * 60 * 1000;
                const diffDays = Math.round(Math.abs((this.checkOutDate - this.checkInDate) / oneDay));
                this.totalPrice = diffDays * this.room.price * this.roomCount;
            } else {
                this.totalPrice = this.room.price * this.roomCount; // 当入住日期或退房日期为空时，将价格设置为房间价格乘以房间数
            }
        },
        sendSelectedRoomIdToBackend() {
            axios.post('http://127.0.0.1:8000/hotels/get_room_and_hotel_info/',
    { roomId: this.selectedRoomId },
    {
        withCredentials: true,
        headers: {
        'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部
    }
    }
)
                .then(response => {
                    const responseData = response.data;
                    console.log('Backend response:', responseData);
                    this.room = responseData.room;
                    this.hotel = responseData.hotel;
                    this.totalPrice = this.room.price * this.roomCount; // 初始化价格为房间价格乘以房间数
                })
                .catch(error => {
                    console.error('Error sending room ID to backend:', error);
                });
        },
        initializeDatePickers() {
            var currentDate = new Date();
            var tomorrowDate = new Date();
            tomorrowDate.setDate(currentDate.getDate() + 1);

            function formatDate(date) {
                var month = date.getMonth() + 1;
                var day = date.getDate();
                return month + '月' + day + '日';
            }

            var picker = new Pikaday({
                field: document.getElementById('checkInDate'),
                trigger: document.getElementById('checkInDate'),
                format: 'YYYY-MM-DD',
                minDate: currentDate,
                onSelect: (date) => {
                    this.checkInDate = date;
                    document.getElementById('checkInDate').textContent = formatDate(date);
                    picker2.setMinDate(new Date(date.getTime() + 24 * 60 * 60 * 1000));
                    this.calculateTotalPrice();
                }
            });

            var picker2 = new Pikaday({
                field: document.getElementById('checkOutDate'),
                trigger: document.getElementById('checkOutDate'),
                format: 'YYYY-MM-DD',
                minDate: tomorrowDate,
                onSelect: (date) => {
                    this.checkOutDate = date;
                    document.getElementById('checkOutDate').textContent = formatDate(date);
                    this.calculateTotalPrice();
                }
            });
        },
        initializeEstimatedArrivalTimeSelect() {
            const now = new Date();
            const currentHour = now.getHours();

            let nextHour = currentHour;
            if (nextHour >= 21) {
                nextHour = 22;
            } else {
                nextHour++;
            }

            const options = [];
            for (let i = nextHour; i < 24; i++) {
                const hour = i < 10 ? `0${i}` : `${i}`;
                options.push({ value: `${hour}:00`, label: `${hour}:00` });
            }
            for (let i = 0; i <= 6; i++) {
                const hour = i < 10 ? `0${i}` : `${i}`;
                options.push({ value: `${hour}:00`, label: `次日 ${hour}:00` });
            }

            this.estimatedArrivalOptions = options;
        },
        formatDate(date) {
            const month = ('0' + (date.getMonth() + 1)).slice(-2);
            const day = ('0' + date.getDate()).slice(-2);
            return month + '-' + day;
        },
        submitForm() {

            var formData = new FormData();
            formData.append('checkInDate', document.getElementById('checkInDate').textContent);
            formData.append('checkOutDate', document.getElementById('checkOutDate').textContent);
            formData.append('roomCount', this.roomCount);
            formData.append('guestName', this.guestName);
            formData.append('email', this.email);
            formData.append('phoneNumber', this.phoneNumber);
            formData.append('estimatedArrivalTime', this.estimatedArrivalTime);
            formData.append('selectedRoomId',this.selectedRoomId)

            console.log(formData);

            // 发送数据到后端
           axios.post('http://127.0.0.1:8000/hotels/hotel_order/', formData, {
    withCredentials: true,

})
.then(response => {
    // 成功处理
    window.location.href = 'http://127.0.0.1:8080/order_success.html';
})
                .catch(error => {
                    // 处理错误
                    console.error(error);
                });
        }
    }
});