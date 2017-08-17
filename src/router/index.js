import Vue from 'vue'
import Router from 'vue-router'
import Category from '@/components/Category'
import Transcripts from '@/components/Transcripts'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Category
    },
    {
      path: '/transcripts',
      component: Transcripts
    }
  ]
})
