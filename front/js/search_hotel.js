document.addEventListener('DOMContentLoaded', function() {
    const results = JSON.parse(localStorage.getItem('searchResults'));
    new Vue({
        el: '#app',
        data: {
            profileUrl: '',
            username: '',
            results: results,
            accessToken:''

        },
        mounted() {
        this.username = this.getCookie('username');
        console.log(this.username);
        console.log('Created hook - Cookie username:', this.username);
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
            logoutfunc: function () {
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
                    })
            },
        }


    });
});