<template>
  <div id="p-category" class="container" style="margin-top: 100px;">
    <div v-for="block in blocks" class="row justify-content-around">
      <div v-for="content in block" class="col-4 p-category-block" :style="{'background-color': content.backgroundColor}">
        <a :href="content.href" class="p-block-link">
          <div class="full-block">
            <icon :name="content.icon"></icon>
            {{content.text}}
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'p-category',
    data () {
      return {
        blocks: [
          [
            {text:"成績", icon:"calendar", backgroundColor: "#34a853", href: "/transcripts"},
            {text:"分析", icon:"line-chart", backgroundColor: "#fbbc05", href: "/"}
          ]
        ]
      }
    }
  }
</script>

<style lang="scss">
  $p-block-height: 200px;
  $p-block-font-size: 48px;
  $p-block-font-color: #292b2c;

  .p-category-block {
    height: $p-block-height;
    line-height: $p-block-height;
    text-align: center;
    font-size: $p-block-font-size;
  }

  #p-category > .row {
    margin: 50px 0;
  }

  .full-block {
    height: 100%;
    width: 100%;
  }

  .p-block-link {
    color: $p-block-font-color;

    &:hover {
      text-decoration: none;
      color: $p-block-font-color;
    }
  }

</style>