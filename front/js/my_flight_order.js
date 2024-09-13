new Vue({
    el: '#app2',
    data: {
        profileUrl: '',
        username: '',
        results: [], // 初始化 results 数据属性
        currentPage: 1, // 当前页数
    pageSize: 2, // 每页显示订单数
    totalOrders: 0, // 总订单数，初始值为 0
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
                } else {
                    return Promise.reject(error);
                }
            }
        );
        this.username = this.getCookie('username');
        console.log(this.username);
        console.log('Created hook - Cookie username:', this.username);

        // 获取用户头像
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

        // 自动运行方法，访问 orders/my_orders
        this.fetchOrders();
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
            var url = 'http://127.0.0.1:8000/user/logout/';
            axios.delete(url, {
                withCredentials: true,
            })
            .then(response => {
                location.href = 'http://127.0.0.1:8080/login.html';
            })
            .catch(error => {
                console.log(error.response);
            })
        },
        fetchOrders() {
            axios.get('http://127.0.0.1:8000/orders/my_flight_orders/', {
                params: {
                    page: this.currentPage, // 传递当前页数作为参数
                    page_size: this.pageSize // 传递每页显示订单数作为参数
                },
                withCredentials: true,
                headers: {
        'Authorization': `Bearer ${this.getCookie('access_token')}`  // 添加 Authorization 头部
    }
            })
            .then(response => {
                // 将获取到的订单数据赋值给 results
                this.results = response.data.results;
                this.totalOrders = response.data.count;
                console.log('Orders fetched:', this.results);
            })
            .catch(error => {
                console.log(error.response);
            });
        },
        handlePageChange(page) {
        // 切换页面时调用 fetchOrders 方法，重新获取数据
        this.currentPage = page;
        this.fetchOrders();
    },
        changePage(page) {
            // 切换页面时调用 fetchOrders 方法，重新获取数据
            this.currentPage = page;
            this.fetchOrders();
        }
    }
});