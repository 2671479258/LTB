// 将 bookRoom 函数添加到全局作用域中
function bookRoom(roomId) {
    // 将房间ID存储在localStorage中
    localStorage.setItem('selectedRoomId', JSON.stringify(roomId));
    // 跳转到新的页面
    window.location.href = 'http://127.0.0.1:8080/hotel_order.html';
}

document.addEventListener('DOMContentLoaded', function() {
    const results = JSON.parse(localStorage.getItem('searchResults'));
    new Vue({
        el: '#app2',
        delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
        data: {
            profileUrl: '',
            username: '',
            results: results // 设置results数据属性
        },
        mounted() {
            this.username = this.getCookie('username');
            console.log('Created hook - Cookie username:', this.username);
            axios.get('http://127.0.0.1:8000/user/get_profile/', {
            withCredentials: true,
            headers: {
        'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部
    }
        })
            .then(response => {
                // 将获取到的头像链接赋值给profileUrl
                this.profileUrl = response.data.profile;
            })
            .catch(error => {
                console.log(error.response);
            });
        },
        methods: {
            getCookie(name) {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) {
                    const cookieValue = parts.pop().split(';').shift();
                    return cookieValue.trim(); // 返回去除空格后的cookie值
                }
            },
            logoutfunc: function() {
                var url = 'http://127.0.0.1:8000/logout/';
                axios.delete(url, {
                    responseType: 'json',
                    withCredentials: true,
                })
                .then(response => {
                    location.href = 'http://127.0.0.1:8080/login.html';
                })
                .catch(error => {
                    console.log(error.response);
                });
            },
            scrollToRoomList() {
                const roomList = document.getElementById('room-list');
                roomList.scrollIntoView({ behavior: 'smooth' });
            },
        }
    });
});