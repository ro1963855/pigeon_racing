<template>
  <div id="p-loading">
     <bounce-loader :loading="loading" :color="color" :size="size"></bounce-loader>
     <div v-if="loading" class="cover_mask"></div> 
  </div>
</template>

<script>
  import BounceLoader from 'vue-spinner/src/BounceLoader.vue';
  import EventHub from "../../../static/js/EventHub";

  export default {
    name: 'p-loading',
    data () {
        return {
        loading: false,
        color: '#5bc0de',
        size: '70px',
        margin: '2px',
        radius: '2px'
        }
    },
    components: {
        BounceLoader
    },
    methods: {
      addLoadingSpinListener () {
        let vm = this;
        EventHub.$on("loading", data => {
            vm.loading = data;
        });
      }
    },
    created() {
        this.addLoadingSpinListener();
    }
  }
</script>

<style>
  .v-spinner {
    position: absolute;
    z-index: 9999;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  .cover_mask {
    position: absolute;
    height: 100%;
    width: 100%;
    background: #000;
    z-index: 9998;
    opacity: 0.4;
  }
</style>