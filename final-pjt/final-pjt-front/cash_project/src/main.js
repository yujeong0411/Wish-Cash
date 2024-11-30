import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import  {  VueperSlides ,  VueperSlide  }  from  'vueperslides' 
import  'vueperslides/dist/vueperslides.css' 
// import { useKakao } from 'vue3-kakao-maps/@utils';

import App from './App.vue'
import router from './router'

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

const app = createApp(App)
app.use(pinia);
app.use(router)
// useKakao('0836119f538d650272fc667d96b1a3e0');

// VueperSlides를 전역 컴포넌트로 등록
app.component('VueperSlides', VueperSlides)
app.component('VueperSlide', VueperSlide)

app.mount('#app')
