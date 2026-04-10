<template>
	<div class="playground">
		<GameMap />
	</div>
</template>

<script type="text/javascript">
	import GameMap from "./GameMap";
	export default{
		components:{
			GameMap
		}
	}
</script>

<style scoped>
	div.playground{
		width: 60vw;
		height: 70vh;
		margin: 30px auto;
	}
</style>