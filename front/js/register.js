var vm = new Vue({
    el: '#app2',
    data: {
        username: '',
        mobile: '',
        password: '',
        password2: '',
        agreeTerms: false,
        usernameError: false,
        passwordError: false,
        mobileError:false
    },
    watch: {
        password(value) {
            this.validatePasswords();
        },
        password2(value) {
            this.validatePasswords();
        },
        username(value){
            this.validateUsername();
        },
        mobile(value){
            this.validateMobile();
        }
    },
    methods: {
        validatePasswords() {
            this.passwordError = this.password !== this.password2;
        },
        validateUsername() {
            this.usernameError = this.username.length<4;
        },
        validateMobile() {
            const mobileRegex = /^1[3-9]\d{9}$/;
            this.mobileError = !mobileRegex.test(this.mobile);
        },
        onSubmit:function () {
            // Final validation before form submission
            this.validatePasswords();
            this.validateUsername();
            this.validateMobile();

            if (this.passwordError) {
                alert('请修正密码错误');
                return;
            }
            if (!this.agreeTerms) {
                alert('请同意服务协议');
                return;
            }


            alert('表单已提交');
            axios.post('http://127.0.0.1:8000/user/register/',
                {
                    username : this.username,
                    password : this.password,
                    mobile : this.mobile
                },

                {
                    responseType: 'json',
                    withCredentials: true,
                })
                .then(response => {
        if (response.data.code === 0) {
            location.href = 'index.html';
        }
        if (response.data.code === 400) {
            alert(response.data.errmsg);
        }
    })
    .catch(error => {
        console.error('There was an error!', error);
        alert('提交失败，请稍后重试。');
    });

        }
    }
});