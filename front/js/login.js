var vm = new Vue({
    el: '#app2',
    data: {
        password: '',
        username: '',
    },




    methods: {


        on_submit: function () {


               axios.post('http://127.0.0.1:8000/user/login/', {
                username: this.username,
                   password:this.password
            }, {
                    responseType: 'json',
                   withCredentials:true,

                })
                    .then(response => {
    if (response.data.code==0) {

       location.href = 'index.html';
    }
    if (response.data.code == 400) {
        alert('输入信息有误')
    }
})


        }
    }
});