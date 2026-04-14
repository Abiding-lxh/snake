<template>
	<PlayGround v-if="$store.state.pk.status==='playing'" />
	<MatchGround v-if="$store.state.pk.status==='matching'" />
</template>

<script type="text/javascript">
import PlayGround from '../components/PlayGround'
import MatchGround from '../components/MatchGround'
import { onMounted,onUnmounted } from 'vue'
import { useStore } from 'vuex'

export default{
	components:{
		PlayGround,
		MatchGround
	},
	setup(){
		const store=useStore();
		const SocketUrl="wss://snake.abiding.cn/wss/multiplayer/?token="+store.state.user.token
		let socket=null;
		onMounted(()=>{
			store.commit("updateOpponent",{
				username:"我的对手",
				photo:"https://cdn.acwing.com/media/article/image/2022/08/09/1_1db2488f17-anonymous.png"
			})
			socket=new WebSocket(SocketUrl);
			
			socket.onopen=()=>{
				console.log("connected!");
				store.commit("updateSocket",socket);
			}

			socket.onmessage=msg=>{
				let data=JSON.parse(msg.data)
				console.log(data)
				let id=data.id;
				if(id==store.state.user.id)return false;
				
				let event=data.event;
				if(event==="start-matching"){
					store.commit("updateOpponent",{
						username:data.username,
						photo:data.photo
					});
					store.commit("updateStatus","playing")
					store.commit("updateGamemap",data.gamemap)
				}
			}
			socket.onclose=()=>{
				console.log("disconnected!");
			}
		})

		onUnmounted(()=>{
			socket.close();
			store.commit("updateStatus","matching")
		})
		return{
			
		}
	}
}
</script>

<style scoped>
	
</style>