var vm = new Vue({
    el: '#app2',
    delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
    data: {
        profileUrl: '',  // 添加一个属性用于保存用户头像链接
        username: '',
        rooms: 1,
        guests: 1,
        showRoomGuestList: false,
        hotelLevels: ['任意级别','一星级', '二星级', '三星级', '四星级', '五星级'],
        selectedHotelLevel: '选择酒店级别',
        showHotelLevelList: false,
        city_list:[],
        accessToken:''


    },
    computed: {
        roomGuestDisplay() {
            return `${this.rooms}间 ${this.guests}位`;
        },
        sortedCityList() {
            // 对城市名称进行排序
            return this.city_list.slice().sort((a, b) => {
                return a.name.localeCompare(b.name, 'zh');
            });
        }
    },
    mounted() {
        this.username = this.getCookie('username');
        console.log(this.username);
        console.log('Created hook - Cookie username:', this.username);
        // 发送 AJAX 请求获取当前登录用户的头像链接
        const accessToken = this.getCookie('access_token');
            console.log('Access Token:', accessToken);
        axios.get('http://127.0.0.1:8000/user/get_profile/', {
            withCredentials: true,
            headers: {
        'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部
    }
        })
        .then(response => {
            // 将获取到的头像链接赋值给 profileUrl

            this.profileUrl = response.data.profile;
        })
        .catch(error => {
            console.log(error.response);
        });

         // 发送 AJAX 请求获取城市列表
        axios.get('http://127.0.0.1:8000/hotels/city_list/', {
            withCredentials: true,
        })
        .then(response => {
            // 将获取到的城市列表赋值给 city_list
            this.city_list = response.data; // 确保响应的数据格式与 this.city_list 兼容
        })
        .catch(error => {
            console.log(error.response);
        });

        document.addEventListener("click", (event) => {
    var cityList = document.getElementById("cityList");
    var destinationInput = document.getElementById("destinationInput");
    var targetElement = event.target;

    if (cityList.style.display === "block" && targetElement !== destinationInput) {
        console.log('456')
        cityList.style.display = "none";
    }





    var roomGuestList = document.getElementById("roomGuestList");
    var roomGuestInput = document.getElementById("roomGuestInput");
    if (roomGuestList && roomGuestInput && roomGuestList.style.display === "block" && targetElement !== roomGuestInput && !roomGuestList.contains(targetElement)) {
        console.log('123')
        this.showRoomGuestList = false;
    }
});


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
            onSelect: function(date) {
                document.getElementById('checkInDate').textContent = formatDate(this.getDate());
            }
        });

        var picker2 = new Pikaday({
            field: document.getElementById('checkOutDate'),
            trigger: document.getElementById('checkOutDate'),
            format: 'YYYY-MM-DD',
            onSelect: function(date) {
                document.getElementById('checkOutDate').textContent = formatDate(this.getDate());
            }
        });

        document.getElementById('checkInDate').textContent = formatDate(currentDate) + ' (今天)';
        document.getElementById('checkOutDate').textContent = formatDate(tomorrowDate) + ' (明天)';
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

        toggleCityList() {
            var cityList = document.getElementById("cityList");
            if (cityList.style.display === "block") {
                cityList.style.display = "none";
            } else {
                cityList.style.display = "block";
            }
        },
        fillCity(city) {
            var destinationInput = document.getElementById("destinationInput");
            destinationInput.value = city;
            var cityList = document.getElementById("cityList");
            cityList.style.display = "none";
        },
        toggleRoomGuestList() {
            this.showRoomGuestList = !this.showRoomGuestList;
        },
        increaseRoom() {
            this.rooms++;
        },
        decreaseRoom() {
            if (this.rooms > 1) {
                this.rooms--;
            }
        },
        increaseGuest() {
            this.guests++;
        },
        decreaseGuest() {
            if (this.guests > 1) {
                this.guests--;
            }
        },
        toggleHotelLevelList() {
            this.showHotelLevelList = !this.showHotelLevelList;
        },
        selectHotelLevel(level) {
            this.selectedHotelLevel = level;
            this.showHotelLevelList = false;
        },

         confirmRoomGuest() {
            event.preventDefault(); // 阻止默认行为
            event.stopPropagation(); // 阻止事件冒泡
        // 这里可以处理确定按钮点击后的逻辑，例如保存数据等
        this.showRoomGuestList = false; // 隐藏房间及住客表单
    },

    submitForm() {
    // 收集表单数据
    var formData = new FormData();
    formData.append('destination', document.getElementById('destinationInput').value);
    formData.append('checkInDate', document.getElementById('checkInDate').textContent);
    formData.append('checkOutDate', document.getElementById('checkOutDate').textContent);
    formData.append('roomGuests', this.roomGuestDisplay);
    formData.append('hotelLevel', this.selectedHotelLevel);

    console.log(formData)
    // 发送数据到后端
    axios.post('http://127.0.0.1:8000/user/hotel/', formData)
        .then(response => {
            const searchResults = response.data.data;

        localStorage.setItem('searchResults', JSON.stringify(searchResults));
        window.location.href = '/search_hotel.html';
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });
},
        logoutfunc: function () {
            var url = 'http://127.0.0.1:8000/user/logout/';
            axios.delete(url, {

                withCredentials:true,
            })
                .then(response => {
                    location.href = 'http://127.0.0.1:8080/login.html';
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
    },
});