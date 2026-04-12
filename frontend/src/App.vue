<template>
  <NavBar />
  <router-view/>
</template>

<script type="text/javascript">
import NavBar from './components/NavBar.vue'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap"

export default{
  name:"App",
  components:{
    NavBar,
  },
  setup:()=>{
    
    // $.ajax({
    //   url:"https://snake.abiding.cn/api/user/register/",
    //   type:"post",
    //   data:{
    //     username:"123",
    //     password:"123",
    //     password_confirm:"123"
    //   },
    //   success(resp){
    //     console.log(resp)
    //   }
    // })


    // $.ajax({
    //   url:"https://snake.abiding.cn/api/token/",
    //   type:"post",
    //   data:{
    //     username:"admin",
    //     password:"123"
    //   },
    //   success(resp){
    //     console.log(resp)
    //     $.ajax({
    //       url:"https://snake.abiding.cn/api/user/getinfo/",
    //       type:"get",
    //       headers:{
    //         'Authorization':"Bearer "+resp.access
    //       },
    //       success(resp){
    //         console.log("hhh",resp)
    //       }
    //     })
    //   },
    //   error(resp){
    //     console.log(resp)
    //   }
    // })
  }
}
</script>

<style>
  body{
    background-image: url("@/assets/images/background.png");
    background-size: cover;
  }

</style>
