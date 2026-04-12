import $ from 'jquery'

export default {
  state: {
    id:"",
    username:"",
    photo:"",
    token:"",
    is_login:false,
    pulling_info:true,
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
      state.id="";
      state.username="";
      state.photo="";
      state.token="";
      state.is_login=false;
    },
    updatePullingInfo(state,pulling_info){
      state.pulling_info=pulling_info;
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
          localStorage.setItem("jwt_token",resp.access)
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
            data.success();
          }else{
            data.error();
          }
        },
        error(){
          data.error();
        }
      })
    },
    logout(context){
      localStorage.removeItem("jwt_token")
      context.commit("logout")
    }
  },
  modules: {
  }
}
