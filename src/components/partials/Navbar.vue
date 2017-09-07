<template>
  <div id="p-navbar">
    <b-navbar toggleable type="light" variant="info" toggle-breakpoint="md">
      <b-navbar-brand class="p_brand" href="/"><icon name="twitter"></icon>Pigeon</b-navbar-brand>
      <b-nav is-nav-bar class="col-md-4 ml-auto">
        <select v-if="isDataReady" class="p-website-select form-control custom-select" @change="websiteSelectOnChange($event.target.value)">
          <optgroup v-for="(websiteValue, websiteKey) in websites" :label="websiteValue.chineseName">
            <option v-for="(groupValue, groupKey) in websiteValue.Group" :value="websiteKey + '|' + groupKey" :selected="groupKey == groupSelected">{{groupValue.chineseName}}</option>
          </optgroup>
        </select>
        <select v-if="isDataReady" class="p-website-select form-control custom-select" @change="pigeonarySelectOnChange($event.target.value)">
          <option v-for="(pigeonaryValue, pigeonaryKey) in websites[websiteSelected].Group[groupSelected].pigenorys" :value="pigeonaryKey" :selected="pigeonaryKey == pigeonarySelected">{{pigeonaryValue.text}}</option>
        </select>
      </b-nav>
    </b-navbar>
  </div>
</template>

<script>
  import Config from '../../../static/js/config.js'
  
  var userRef = firebase.database().ref('/users/' + Config.username);
  var websitesRef = firebase.database().ref('/websites');

  export default {
    name: 'p-navbar',
    data () {
      return {
        websiteSelected: null,
        groupSelected: null,
        pigeonarySelected: null,
        websites: null,
        isDataReady: false
      }
    },
    watch: {
      websiteSelected: function(val, oldVal){
        if (oldVal != null) {
          userRef.update({
            websiteSelected: val
          })

        }

      },
      groupSelected: function(val, oldVal){
        if (oldVal != null) {
          userRef.update({
            groupSelected: val
          })

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
        getWebsitesData () {
          let vm = this;
          websitesRef.once('value', function(snapshot){
            vm.websites = snapshot.val();
            vm.checkUserRecord();
          })
        },
        checkUserRecord () {
          let vm = this;
          let website = this.getObjectByIndex(this.websites, 0);
          let websiteSelected = website.key;
          let group = this.getObjectByIndex(website.obj.Group, 0);
          let groupSelected = group.key; 
          let pigeonary = this.getObjectByIndex(group.obj.pigenorys, 0);                   
          let pigeonarySelected = pigeonary.key;
          userRef.once('value', function(snapshot){
            let val = snapshot.val();
            if (val === null) {
              vm.addUserInfo(username, websiteSelected, groupSelected, pigeonarySelected);
            }
            else {
              websiteSelected = val.websiteSelected;
              groupSelected = val.groupSelected;
              pigeonarySelected = val.pigeonarySelected;
            }

            vm.websiteSelected = websiteSelected;
            vm.groupSelected = groupSelected;
            vm.pigeonarySelected = pigeonarySelected;
            vm.isDataReady = true;
          })

        },
        addUserInfo (username, websiteSelected, groupSelected, pigeonarySelected) {
          userRef.set({
            websiteSelected: websiteSelected,
            groupSelected: groupSelected,
            pigeonarySelected: pigeonarySelected
          })
        },
        websiteSelectOnChange (websiteSelect) {
          var websiteSelectSplit = websiteSelect.split("|");
          this.websiteSelected = websiteSelectSplit[0];
          this.groupSelected = websiteSelectSplit[1];
          let pigeonary = this.getObjectByIndex(this.websites[this.websiteSelected].Group[this.groupSelected].pigenorys, 0);
          this.pigeonarySelected = pigeonary.key;
        },
        pigeonarySelectOnChange (pigeonarySelect) {
          this.pigeonarySelected =  pigeonarySelect;
        },
        getObjectByIndex (obj, index) {
          var keys = Object.keys( obj );
          return {obj: obj[keys[index]], key: keys[index]};
        }
    },
    created () {
      this.getWebsitesData();
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