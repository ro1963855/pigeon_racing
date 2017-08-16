import Vue from 'vue'
import Router from 'vue-router'
import Category from '@/components/Category'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: Category
    }
  ]
})
