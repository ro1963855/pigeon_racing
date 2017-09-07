<template>
  <div id="app">
    <LoadingSpin></LoadingSpin>
    <Navbar></Navbar>
    <router-view></router-view>
  </div>
</template>

<script>
  import Navbar from './components/partials/Navbar'
  import LoadingSpin from './components/partials/LoadingSpin'
  
  export default {
    name: 'app',
    data () {
      return {
      }
    },
    components: {
      Navbar,
      LoadingSpin
    }
  }

</script>