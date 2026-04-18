<template>
	<div class="container">
		<div class="player-info" >
			<div class="player-a-info" v-if="!$store.state.record.is_record">
				玩家A：{{ a_username }}
			</div>
		</div>
		<div ref="parent" class="gamemap">
			<canvas ref="canvas" tabindex="0"></canvas>
		</div>
		<div class="player-info" >
			<div class="player-b-info" v-if="!$store.state.record.is_record">
				玩家B:{{ b_username }}
			</div>
		</div>
	</div>
	
</template>

<script type="text/javascript">
import { GameMap } from '@/assets/scripts/GameMap'
import { ref,onMounted } from 'vue'
import { useStore } from 'vuex'
export default{
	setup(){
		const store=useStore()
		let parent=ref(null);
		let canvas=ref(null);

		let id=store.state.user.id

		let a_username=ref("")
		let a_photo=ref("")
		let b_username=ref("")
		let b_photo=ref("")


		const judge_player=()=>{
			console.log(typeof(id))
			console.log(typeof(store.state.pk.a_id))
			if(id===store.state.pk.a_id){
				a_username.value=store.state.user.username
				a_photo.value=store.state.user.photo
				b_username.value=store.state.pk.opponent_username
				b_photo.value=store.state.pk.opponent_photo
			}else if(id===store.state.pk.b_id){
				b_username.value=store.state.user.username
				b_photo.value=store.state.user.photo
				a_username.value=store.state.pk.opponent_username
				a_photo.value=store.state.pk.opponent_photo
			}
			console.log(a_username,a_photo)
		}


		onMounted(()=>{
			store.commit(
				"updateGameObject",
				new GameMap(canvas.value.getContext('2d'),parent.value,store)
			);
			judge_player();
		})

		return{
			parent,
			canvas,
			a_username,
			a_photo,
			b_username,
			b_photo
		}
	}
}
</script>


<style scoped>
div.gamemap{
	width: 70%;
	height: 100%;
	display: flex;
	justify-content: center;
	align-content: center;
	z-index: 1;
}
div.container{
	width: 100%;
	height: 100%;
	display: flex;
	position: relative;
}
div.player-info{
	width: 15%;
/*	background-color: blue;*/
	z-index: 2;
	color: white;
	font-size: 24px;
	font-weight: 400;
}
div.player-a-info{
	position: absolute;
	bottom: 0vh;
	left: 5%;
	height: 10vh;
	width: 10vw;
	background-color: rgba(50, 50, 50, 0.5);
}
div.player-b-info{
	position: absolute;
	top:0vh;
	right: 5%;
	height: 10vh;
	width: 10vw;
	background-color: rgba(50, 50, 50, 0.5);
}

</style>