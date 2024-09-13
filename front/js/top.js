var vm = new Vue({
    el: '#app2',
    delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
    data: {
        profileUrl: '',  // 添加一个属性用于保存用户头像链接
        username: '',

    },

    mounted() {
        this.username = this.getCookie('username');
        console.log(this.username);
        console.log('Created hook - Cookie username:', this.username);
        // 获取用户资料
        axios.get('http://127.0.0.1:8000/user/get_profile/', {
            withCredentials: true,
            headers: {
        'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部
    },
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