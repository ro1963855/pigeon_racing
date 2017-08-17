<template>
  <div id="p-navbar">
    <b-navbar toggleable type="light" variant="info" toggle-breakpoint="md">
      <b-navbar-brand class="p_brand" href="/"><icon name="twitter"></icon>Pigeon</b-navbar-brand>
      <b-nav is-nav-bar class="col-md-4 ml-auto">
        <b-form-select class="p-website-select" v-if="isDataReady" v-model="websiteSelected" :options="websites">
        </b-form-select>
        <b-form-select class="p-website-select" v-if="isDataReady" v-model="pigeonarySelected" :options="websites[websiteSelected].pigeonarys">
        </b-form-select>
      </b-nav>
    </b-navbar>
  </div>
</template>

<script>
  var username = 'dad';
  var userRef = firebase.database().ref('/users/' + username);

  export default {
    name: 'p-navbar',
    data () {
      return {
        websiteSelected: null,
        pigeonarySelected: null,
        isDataReady: false,
        message: 0,
        websites: [
          {value: '0', text: "鴿神一號", pigeonarys:[{value: '27', text: "永靖中山傳訊(冬)"}]},
          {value: '1', text: "嶺東資訊", pigeonarys:[{value: '1606', text: "金溪湖鴿會"}]}
        ]
      }
    },
    watch: {
      websiteSelected: function(val, oldVal){
        if (oldVal != null) {
          userRef.update({
            websiteSelected: val
          })

          this.pigeonarySelected = this.websites[val].pigeonarys[0].value;
        }

      },
      pigeonarySelected: function(val, oldVal){
        if (oldVal != null) {
          userRef.update({
            pigeonarySelected: val
          })
        }
      }
    },
    methods: {
        checkUserRecord () {
          let vm = this;
          let websiteSelected = this.websites[0].value;
          let pigeonarySelected = this.websites[0].pigeonarys[0].value;
          userRef.once('value', function(snapshot){
            let val = snapshot.val();
            if (val === null) {
              vm.addUserInfo(username, websiteSelected, pigeonarySelected);
            }
            else {
              websiteSelected = val.websiteSelected;
              pigeonarySelected = val.pigeonarySelected;
            }

            vm.websiteSelected = websiteSelected;
            vm.pigeonarySelected = pigeonarySelected;
            vm.isDataReady = true;
          })

        },
        addUserInfo (username, websiteSelected, pigeonarySelected) {
          userRef.set({
            websiteSelected: websiteSelected,
            pigeonarySelected: pigeonarySelected
          })
        }
    },
    created () {
      this.checkUserRecord();
    }
  }
</script>

<style>
  .fa-icon {
    width: auto;
    height: 1em;
  }

  .p_brand {
    color: #fff !important;
    font-size: 36px;
  }

  .p-website-select {
    margin-right: 10px;
  }
</style>