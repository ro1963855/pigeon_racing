// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
import BootstrapVue from 'bootstrap-vue';
import Icon from 'vue-awesome/components/Icon';
import VueResource from 'vue-resource';
import 'vue-awesome/icons'
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';

Vue.use(BootstrapVue);
Vue.component('icon', Icon);
Vue.use(VueResource);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})