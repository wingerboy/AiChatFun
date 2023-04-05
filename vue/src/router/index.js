import Vue from "vue";
import Router from "vue-router";
import routes from "./config";

Vue.use(Router);

export const router =  new Router({
  routes
});


// 路由守卫
router.beforeEach((to, from, next) => {
  console.log(to.name);
  console.log(from);
  next();
});

router.afterEach((to, from) => {
  console.log('路由变动')
  console.log(to, from);
});

export default router;