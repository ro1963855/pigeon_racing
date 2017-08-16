<template>
  <div id="p-category" class="container" style="margin-top: 100px;">
    <div class="row justify-content-around">
      <div class="col-4 p-category-block" style="background-color: #34a853;">
        成績
      </div>
      <div class="col-4 p-category-block" style="background-color: #fbbc05;">
        分析
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'p-category',
    data () {
      return {
        
      }
    }
  }
</script>

<style>
  .p-category-block {
    height: 200px;
    line-height: 200px;
    text-align: center;
  }

  #p-category > .row {
    margin: 50px 0;
  }

</style>