<template>
    <ContentField>
        <div class="row justify-content-md-center">
        <div class="col-3">
            <form @submit.prevent="register">
                <div class="mb-3">
                  <label for="username" class="form-label">用户名</label>
                  <input v-model="username" type="text" class="form-control" id="username" placeholder="请输入用户名">
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">密码</label>
                  <input v-model="password" type="password" class="form-control" id="password" placeholder="请输入密码">
                </div>
                <div class="mb-3">
                  <label for="password_confirm" class="form-label">密码</label>
                  <input v-model="password_confirm" type="password" class="form-control" id="password_confirm" placeholder="请再次输入密码">
                </div>
                <div class="error-message"> {{ error_message }} </div>
                <button type="submit" class="btn btn-primary">注册</button>
            </form>
        </div>
        </div>
    </ContentField>
</template>

<script type="text/javascript">
import ContentField from '../components/ContentField'
import { ref } from 'vue'
import router from '../router/index'
import $ from 'jquery'

export default{
    components:{
        ContentField
    },
    setup(){
        let username=ref('');
        let password=ref('');
        let password_confirm=ref('');
        let error_message=ref('')

        const register=()=>{
            error_message.value="";
            $.ajax({
                url:"https://snake.abiding.cn/api/user/register/",
                type:'post',
                data:{
                    username:username.value,
                    password:password.value,
                    password_confirm:password_confirm.value
                },
                success(resp){
                    if(resp.result==="success"){
                        router.push({name:"user_login_view"})
                    }else{
                        error_message.value=resp.result;
                    }
                },
            })
        }

        return{
            username,
            password,
            password_confirm,
            error_message,
            register
        }
    }
}
</script>

<style scoped>
button{
    width: 100%;
}
div.error-message{
    color: red;
}
</style>