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
			<ul class="navbar-nav">
				<li class="nav-item dropdown">
					<a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
						lxh
					</a>
					<ul class="dropdown-menu">
						<li><router-link class="dropdown-item" :to="{name:'user_bot_view'}">我的Bot</router-link></li>
						<li><hr class="dropdown-divider"></li>
						<li><a class="dropdown-item" href="#">退出</a></li>
					</ul>
				</li>
			</ul>
		</div>
	</div>
</nav>
</template>

<script type="text/javascript">
	import { useRoute } from 'vue-router'
	import { computed } from 'vue'
		export default{
			setup(){
				const route = useRoute();
				let route_name=computed(()=>route.name);
				return {
					route_name
				}
			}
		}
</script>

<style scoped>
		
</style>