import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export default new VueRouter({

  routes: [{
    id: 1,
    path: '/',
    name: '登录页面',
    component: require("../views/login.vue").default
  }]
});