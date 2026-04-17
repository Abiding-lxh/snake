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
	width: 80vw;
	height: 80vh;
	margin: 30px auto;
/*	background-color: lightblue;*/
}

</style>