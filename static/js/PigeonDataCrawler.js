import Vue from 'vue';
import EventHub from "./EventHub";
import moment from "moment";

let websitesRef = firebase.database().ref('/websites');

export default {
    getPigeonData: function(websiteSelected, groupSelected, pigeonarySelected) {
        let vm = this;
        EventHub.$emit('loading', true);
        websitesRef.child(websiteSelected + "/Group/" + groupSelected + "/pigenorys/" + pigeonarySelected).once('value', function(snapshot) {
            let val = snapshot.val();
            let startDate = vm.getStartDate(val.update);
            vm.callCrawlerAPI(websiteSelected, groupSelected, pigeonarySelected, val.val, startDate);
        })
    },
    callCrawlerAPI: function(websiteSelected, groupSelected, pigeonarySelected, union, date) {
        // EventHub.$emit('loading', true);
        let vm = this;
        let inputDate = moment(date).format("YYYY/MM/DD");
        console.log(inputDate);
        Vue.http.post("/data/data/" + websiteSelected, {union: union, date: inputDate})
        .then((response) => {
            console.log(response.data);
            vm.saveRecord(websiteSelected, groupSelected, pigeonarySelected, date, response.data);
            date = vm.addOneDate(date);
            if (date !== false) {
                vm.callCrawlerAPI(websiteSelected, groupSelected, pigeonarySelected, union, date);
            }
            else {
                EventHub.$emit('loading', false);
            }

        }).catch((response) => {
        }).finally(() => {
        
        });

    },
    getStartDate: function(startDate) {
        if(startDate == null) {
            moment.locale();
            startDate = moment().subtract(1, 'year').format("YYYY-MM-DD");
        }

        return startDate;
    },
    addOneDate: function(date) {
        let newDate = moment(date).add(1, 'days').format("YYYY-MM-DD");
        if (!moment().isAfter(date, 'day')) {
            return false;
        }

        return newDate;
    },
    saveRecord: function(websiteSelected, groupSelected, pigeonarySelected, date, record) {
        let pigenorysRef = websitesRef.child(websiteSelected + "/Group/" + groupSelected + "/pigenorys/" + pigeonarySelected);
        let key = moment(date).format("YYYY/MM/DD");
        pigenorysRef.update({update: moment().format("YYYY/MM/DD HH:mm:ss")});
        record = {[date]: record[key]};
        pigenorysRef.child("record").update(record);
    }
}; 