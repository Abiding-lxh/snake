<!DOCTYPE html>
<template>
<nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
	<div class="container">
		<router-link class="navbar-brand" :to="{name:'home'}">Snake</router-link>
		<div class="collapse navbar-collapse" id="navbarText">
			<ul class="navbar-nav me-auto mb-2 mb-lg-0">
				<li class="nav-item">
					<router-link :class="router_name=='pk_view'?'nav-link active':'nav-link'" :to="{name:'pk_view'}">对战</router-link>
				</li>
				<li class="nav-item">
					<router-link :class="router_name=='record_view'?'nav-link active':'nav-link'" :to="{name:'record_view'}">对局列表</router-link>
				</li>
				<li class="nav-item">
					<router-link :class="router_name=='ranklist_view'?'nav-link active':'nav-link'" :to="{name:'ranklist_view'}">排行榜</router-link>
				</li>
			</ul>
			<ul class="navbar-nav" v-if="$store.state.user.is_login">
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
						{{ $store.state.user.username }}
					</a>
					<ul class="dropdown-menu">
						<li><router-link class="dropdown-item" :to="{name:'user_bot_view'}">我的Bot</router-link></li>
						<li><hr class="dropdown-divider"></li>
						<li><a class="dropdown-item" href="#" @click="logout">退出</a></li>
					</ul>
				</li>
			</ul>
			<ul class="navbar-nav" v-else-if="!$store.state.user.pulling_info">
				<li class="nav-item">
					<router-link class="nav-link" :to="{ name:'user_login_view' }" role="button">
						登录
					</router-link>
				</li>
				<li class="nav-item">
					<router-link class="nav-link" :to="{ name:'user_register_view' }" role="button">
						注册
					</router-link>
				</li>
			</ul>
		</div>
	</div>
</nav>
</template>

<script type="text/javascript">
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { useStore } from 'vuex'
export default{
	setup(){
		const route = useRoute();
		const store = useStore();
		let route_name=computed(()=>route.name);

		const logout=()=>{
			store.dispatch("logout")
		}
		return {
			route_name,
			logout
		}
	}
}
</script>

<style scoped>
		
</style>