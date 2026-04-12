import $ from 'jquery'

export default {
  state: {
    id:"",
    username:"",
    photo:"",
    token:"",
    is_login:false,
  },
  getters: {
  },
  mutations: {
    updateUser(state,user){
      state.id=user.id;
      state.username=user.username;
      state.photo=user.photo;
      state.is_login=user.is_login;
    },
    updateToken(state,token){
      state.token=token;
    },
    logout(state){
      state.id="",
      state.username="",
      state.photo="",
      state.token="",
      state.is_login=false
    }
  },
  actions: {
    login(context,data){
      $.ajax({
        url:"https://snake.abiding.cn/api/token/",
        type:"post",
        data:{
          username:data.username,
          password:data.password
        },
        success(resp){
          context.commit("updateToken",resp.access)
          data.success(resp);
        },
        error(resp){
          data.error(resp)
        }
      })
    },
    getinfo(context,data){
      $.ajax({
        url:"https://snake.abiding.cn/api/user/getinfo/",
        type:"get",
        headers:{
          'Authorization':"Bearer "+context.state.token
        },
        success(resp){
          if(resp.result==="success"){
            context.commit("updateUser",{
              ...resp,
              is_login:true
            });
            data.success(resp);
          }else{
            data.error(resp);
          }
        },
        error(resp){
          data.error(resp);
        }
      })
    },
    logout(context){
      context.commit("logout")
    }
  },
  modules: {
  }
}
