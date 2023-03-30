import Vue from "vue";
import Router from "vue-router";
import Index from "./views/Index.vue";

Vue.use(Router);

const router = new Router({
  mode: "hash",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "index",
      component: Index,
    },
  ],
});
router.beforeEach((to, from, next) => {
  //console.log(to.name);
  //console.log(from);
  next();
});
export default router;
