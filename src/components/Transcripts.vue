<template>
  <div id="p-transcripts" class="container" style="margin-top: 100px;">
    <div id="dateSelector" class="row" v-if="isDataReady">
      <b-form-select v-model="dateSelect.selected" :options="dateSelect.options" class="col-md-2"></b-form-select>
      <b-form-select v-model="pigeonry.selected" :options="pigeonry.options" class="col-md-2"></b-form-select>
      <span v-if="isDataReady" class="col-md-6 align-self-end"><p>資料更新時間：{{record.updateTime}}</p></span>
    </div>
    <div style="margin-top: 20px;"></div>
    <div class="row" v-if="isDataReady">
      <b-table striped hover show-empty :items="record.tableData" :fields="record.fieldKey"></b-table>
    </div>
  </div>

</template>

<script>
  import PigeonDataCrawler from '../../static/js/PigeonDataCrawler.js';
  import Config from '../../static/js/config.js';
  import EventHub from "../../static/js/EventHub";

  var userRef = firebase.database().ref('/users/' + Config.username);
  let websitesRef = firebase.database().ref('/websites');

  export default {
    name: 'p-transcripts',
    props: ['loading'],
    data () {
      return {
        websiteSelected: undefined,
        groupSelected: undefined,
        pigeonarySelected: undefined,
        isDataReady: false,
        record: {
          completeData: undefined,
          tableData: undefined,
          fieldKey: {
            totalRank:    {label: '序號', sortable: true, 'class': 'text-center'},
            selfRank:     {label: '序號2', sortable: true, 'class': 'text-center'},
            pigeonryID:   {label: '會員編號', sortable: true, 'class': 'text-center'},
            pigeonID:     {label: '腳環號碼', 'class': 'text-center'},
            arriveTime:   {label: '鴿鐘時間', 'class': 'text-center'}
          },
          updateTime: undefined
        },
        dateSelect: {
          options: undefined,
          selected: undefined
        },
        pigeonry: {
          options: undefined,
          selected: undefined,          
        }
      }
    },
    watch: {
      pigeonarySelected: function(val, oldVal) {
        PigeonDataCrawler.getPigeonData(this.websiteSelected, this.groupSelected, this.pigeonarySelected);
      },
      "dateSelect.selected": function(val, oldVal) {
        this.getTableData(val, this.pigeonry.selected);
      },
      "pigeonry.selected": function(val, oldVal) {
        this.getTableData(this.dateSelect.selected, val);
      }
    },
    methods: {
      addUserInfoListener() {
        let vm = this;
        userRef.on('value', function(snapshot) {
          let val = snapshot.val();
          if (val !== null) {
            vm.websiteSelected = val.websiteSelected;
            vm.groupSelected = val.groupSelected;
            vm.pigeonarySelected = val.pigeonarySelected;
          }

        })
      },
      addLoadingSpinListener() {
        let vm = this;
        EventHub.$on("loading", data => {
            if (data === false) {
              vm.setRecordData();
            }

        });
      },
      setRecordData() {
        let vm = this;
        websitesRef.child(vm.websiteSelected + "/Group/" + vm.groupSelected + "/pigenorys/" + vm.pigeonarySelected).on('value', function(snapshot) {
          let val = snapshot.val();
          vm.dateSelect.options = Object.keys(val.record).sort().reverse();
          if (vm.dateSelect.selected == undefined) {
            vm.dateSelect.selected = vm.dateSelect.options[0];
          }

          vm.record.completeData = vm.getTableDataFormat(val.record);
          vm.record.updateTime = val.update;
          vm.pigeonry.options = vm.getPigeonList(vm.record.completeData);
          if (vm.dateSelect.pigeonrys == undefined) {
            vm.pigeonry.selected = "";
          }
          
          vm.isDataReady = true;
        })
      },
      getTableDataFormat(firebaseData) {
        Object.keys(firebaseData).map(function(firebaseKey) { 
          firebaseData[firebaseKey] = Object.keys(firebaseData[firebaseKey]).map(key => firebaseData[firebaseKey][key]);
        });

        return firebaseData;
      },
      getPigeonList(firebaseData) {
        let totoalArray = [];
        let pigeonaryList = [];
        Object.keys(firebaseData).map(function(key) { 
          firebaseData[key].forEach(function(element) {
            pigeonaryList.push(element.pigeonryID);
          });
        });

        return [{text: "全部", value: ""}].concat(Array.from(new Set(pigeonaryList)).sort());
      },
      getTableData(dateSelect, pigeonrySelect) {
        let vm = this;
        let dataCollection = [];
        let tableData = vm.record.completeData[dateSelect];

        if (pigeonrySelect != "" && pigeonrySelect != undefined) {
          Object.keys(tableData).map(function(key) { 
            if (tableData[key].pigeonryID === pigeonrySelect) {
              dataCollection.push(tableData[key]);
            }
          });
        }
        else {
          dataCollection = vm.record.completeData[dateSelect];
        }

        vm.record.tableData = dataCollection;
      }
    },
    created () {
      this.addLoadingSpinListener();
      this.addUserInfoListener();
    }
  }
</script>

<style>
  #dateSelector > select {
    margin-right: 10px;
  }
</style>