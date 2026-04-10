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

    }
  }
</script>

<style>
  body{
    background-image: url("@/assets/images/background.png");
    background-size: cover;
  }

</style>
