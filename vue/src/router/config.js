import Home from '../views/Home/Home';
// import Other from '../views/Other/Other';

const routes = [
//   {
//     path: '/',
//     redirect: '/home'
//   },
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: '首页'
    }
  },
  // {
  //   path: '/other',
  //   name: 'other',
  //   component: Other,
  //   meta: {
  //     title: '首页'
  //   }
  // }
]

export default routes;