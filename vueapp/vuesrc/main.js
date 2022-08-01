import { createApp } from 'vue'
import App from './App.vue'

import BusRouteList from "@/components/BusRouteList"
// import BusRouteItem from "@/components/BusRouteItem"

import { createRouter, createWebHistory } from "vue-router";
import axios from "./api.js";

const routes = [
  { path: '/transport/routes/', component: BusRouteList },
  // { path: '/transport/routes/:pk/', component: BusRouteItem }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

let app = createApp(App);
app.config.globalProperties.$axios = axios;

app.use(router);

app.mount('#vueapp_container');
