import { createRouter, createWebHistory } from 'vue-router'
import PkView from '../views/PkView'
import RecordView from '../views/RecordView'
import RankListView from '../views/RankListView'
import UserBotView from '../views/UserBotView'
import NotFound from '../views/NotFound'

import LoginView from '../views/LoginView'
import RegisterView from '../views/RegisterView'

import store from '../store/index'

const routes = [
  {
    path:'/',
    name:"home",
    redirect:"/pk",
    meta:{
      requestAuth:true,
    }
  },
  {
    path:"/pk/",
    name:"pk_view",
    component:PkView,
    meta:{
      requestAuth:true,
    }
  },
  {
    path:"/record/",
    name:"record_view",
    component:RecordView,
    meta:{
      requestAuth:true,
    }
  },
  {
    path:"/ranklist/",
    name:"ranklist_view",
    component:RankListView,
    meta:{
      requestAuth:true,
    }
  },
  {
    path:"/user/login/",
    name:"user_login_view",
    component:LoginView,
    meta:{
      requestAuth:false,
    }
  },
  {
    path:"/user/register",
    name:"user_register_view",
    component:RegisterView,
    meta:{
      requestAuth:false,
    }
  },
  {
    path:"/user/bot/",
    name:"user_bot_view",
    component:UserBotView,
    meta:{
      requestAuth:true,
    }
  },
  {
    path:"/404/",
    name:"404",
    component:NotFound,
    meta:{
      requestAuth:false,
    }
  },
  {
    path:"/:catchAll(.*)",
    redirect:"/404/"
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to,from,next)=>{
  if(to.meta.requestAuth&&!store.state.user.is_login){
    next({name:"user_login_view"})
  }else{
    next();
  }
})

export default router