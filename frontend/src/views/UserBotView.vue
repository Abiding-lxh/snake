<template>
    <ContentField>
        我的bot
    </ContentField>
</template>

<script type="text/javascript">
import ContentField from '../components/ContentField'
import $ from 'jquery'
import { useStore } from 'vuex'

export default{
    components:{
        ContentField
    },
    setup(){
        const store=useStore()
        $.ajax({
          url:"https://snake.abiding.cn/api/bot/list/",
          type:"get",

          headers:{
            'Authorization':"Bearer "+store.state.user.token,
          },
          success(resp){
            console.log(resp)
          },
          error(resp){
            console.log(resp)
          }
        })
        // $.ajax({
        //   url:"https://snake.abiding.cn/api/bot/update/",
        //   type:"post",
        //   data:{
        //     bot_id:1,
        //     title:"dfsfsf",
        //     description:"fffffffffff",
        //     content:"tsfeef",
        //   },
        //   headers:{
        //     'Authorization':"Bearer "+store.state.user.token,
        //   },
        //   success(resp){
        //     console.log(resp)
        //   },
        //   error(resp){
        //     console.log(resp)
        //   }
        // })
        // $.ajax({
        //   url:"https://snake.abiding.cn/api/bot/remove/",
        //   type:"post",
        //   data:{
        //     bot_id:5
        //   },
        //   headers:{
        //     'Authorization':"Bearer "+store.state.user.token,
        //   },
        //   success(resp){
        //     console.log(resp)
        //   },
        //   error(resp){
        //     console.log(resp)
        //   }
        // })
        // $.ajax({
        //   url:"https://snake.abiding.cn/api/bot/add/",
        //   type:"post",
        //   data:{
        //     title:"123",
        //     description:"",
        //     content:"test",
        //   },
        //   headers:{
        //     'Authorization':"Bearer "+store.state.user.token,
        //   },
        //   success(resp){
        //     console.log(resp)
        //   },
        //   error(resp){
        //     console.log(resp)
        //   }
        // })
    }
}
</script>

<style scoped>
    
</style>