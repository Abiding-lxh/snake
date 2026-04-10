import { createRouter, createWebHistory } from 'vue-router'
import PkView from '../views/PkView'
import RecordView from '../views/RecordView'
import RankListView from '../views/RankListView'
import UserBotView from '../views/UserBotView'
import NotFound from '../views/NotFound'

const routes = [
  {
    path:'/',
    name:"home",
    redirect:"/pk",

  },
  {
    path:"/pk/",
    name:"pk_view",
    component:PkView,
  },
  {
    path:"/record/",
    name:"record_view",
    component:RecordView,
  },
  {
    path:"/ranklist/",
    name:"ranklist_view",
    component:RankListView,
  },
  {
    path:"/user/bot/",
    name:"user_bot_view",
    component:UserBotView,
  },
  {
    path:"/404/",
    name:"404",
    component:NotFound,
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

export default router