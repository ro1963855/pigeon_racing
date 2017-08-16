<template>
  <div id="p-navbar">
    <b-navbar toggleable type="light" variant="info" toggle-breakpoint="md">
      <b-navbar-brand class="p_brand" href="/"><icon name="twitter"></icon>Pigeon</b-navbar-brand>
      <b-nav is-nav-bar class="ml-auto col-md-4">
        <b-form-select v-model="selected" :options="pigeonrys" right>
        </b-form-select>
      </b-nav>
    </b-navbar>
  </div>
</template>

<script>
  export default {
    name: 'p-navbar',
    data () {
      return {
        selected: 2,
        pigeonrys: [
          {value: null, text: "選擇鴿會"},
          {value: '1', text: "嶺東資訊"},
          {value: '2', text: "鴿神一號"}
        ]
      }
    }
  }
</script>

<style>
  .fa-icon {
    width: auto;
    height: 1em; /* or any other relative font sizes */
  }

  .p_brand {
    color: #fff !important;
    font-size: 36px;
  }
</style>