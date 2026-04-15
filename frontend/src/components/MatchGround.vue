<template>
    <div class="matchground">
        <div class="row">
            <div class="col-4">
                <div class="user-photo">
                    <img :src="$store.state.user.photo">
                </div>
                <div class="user-username">
                    {{ $store.state.user.username }}
                </div>
            </div>
            <div class="col-4">
                <div class="user-select-bot">
                    <select v-model="select_bot" class="form-select" aria-label="Default select example">
                      <option value=-1>亲自出马</option>
                      <option v-for="bot in bots" :key="bot.id" :value="bot.id">{{ bot.title }}</option>
                    </select>
                </div>
            </div>
            <div class="col-4">
                <div class="user-photo">
                    <img :src="$store.state.pk.opponent_photo">
                </div>
                <div class="user-username">
                    {{ $store.state.pk.opponent_username }}
                </div>
            </div>
        </div>
        <div class="col-12" style="text-align: center;padding-top: 10vh;">
            <button @click="click_match_btn" type="button" class="btn btn-warning">{{ match_btn_info }}</button>
        </div>
    </div>
</template>

<script type="text/javascript">

import { ref } from 'vue'
import { useStore } from 'vuex'
import $ from 'jquery'
export default{

    setup(){
        const store=useStore();
        let match_btn_info=ref("开始匹配");
        let bots=ref([])
        let select_bot=ref(-1)

        const click_match_btn=()=>{
            if(match_btn_info.value==="开始匹配"){
                match_btn_info.value="取消";
                console.log(select_bot.value)
                store.state.pk.socket.send(JSON.stringify({
                    event:"start-matching",
                    bot_id:select_bot.value,
                }))
            }else{
                match_btn_info.value="开始匹配";
                store.state.pk.socket.send(JSON.stringify({
                    event:"stop-matching",
                }))
            }
        }
        const refresh_bots=()=>{
            $.ajax({
              url:"https://snake.abiding.cn/api/bot/list/",
              type:"get",
              headers:{
                'Authorization':"Bearer "+store.state.user.token,
              },
              success(resp){
                console.log(resp)
                bots.value=resp.bots
              },
            })
        }
        refresh_bots();

        return{
            match_btn_info,
            click_match_btn,
            bots,
            select_bot
        }
    }
}
</script>

<style scoped>
div.matchground{
    width: 50vw;
    height: 60vh;
    margin: 30px auto;
    background-color: rgba(50,50,50,0.5);
}
div.user-photo{
    padding-top: 10vh;
    text-align: center;
}
div.user-photo>img{
    width: 30%;
    border-radius: 50%;
}
div.user-username{
    padding-top: 3vh;
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    color: white;
}
div.user-select-bot{
    padding-top: 20vh;
}
div.user-select-bot>select{
    width:70%;
    margin: 0 auto;
}
</style>