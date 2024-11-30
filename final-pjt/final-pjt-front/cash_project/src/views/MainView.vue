<template>
  <header class="header-container">
    <div class="header-text">
      <h1 class="main-title">당신의 금융 소망을 현실로,<br/><span class="highlight">Wish Cash</span></h1>
      <h3 class="sub-title">당신의 소망에 든든한 디딤돌이 되겠습니다.</h3>
    </div>
    <div class="slider-container">
      <vueper-slides
        class="no-shadow"
        :visible-slides="1"
        :slide-ratio="1/2"
        :dragging-distance="70"
        :bullets="true"
        :autoplay="true"
        :infinite="true"
        :duration="3000"
        :pause-on-hover="true"
        :arrows="true"
        fixed-height="300px"
        @click="handleSlideClick"
      >
        <vueper-slide
          v-for="(slide, i) in slides"
          :key="i"
          :image="slide.image"
          :title="slide.title"
          class="cursor-pointer"
        >
        </vueper-slide>

        <template #arrow-left>
          <button class="custom-arrow left">
            <span class="arrow-icon">〈</span>
          </button>
        </template>

        <template #arrow-right>
          <button class="custom-arrow right">
            <span class="arrow-icon">〉</span>
          </button>
        </template>
      </vueper-slides>
    </div>
  </header>

  <div class="banner">
    <div class="products-container">
      <div class="content-wrapper">
        <h2 class="products-title">금융상품</h2>
        <div class="layout-container">
          <div class="menu-container">
            <div
              v-for="(item, index) in menuItems"
              :key="index"
              @click="handleMenuClick(item)"
              class="menu-item group"
              :class="{ 'cursor-pointer': item.type === 'modal' }"
            >
              <div class="icon-container">
                <component :is="item.icon" size="32" color="white" class="icon-white" />
              </div>
              <span class="menu-label">{{ item.label }}</span>
            </div>
          </div>
          <div class="image-container">
            <img src="@/assets/mainbanner.jpeg" alt="banner" class="banner-image">
          </div>
        </div>
      </div>
    </div>
  </div>

    <!-- Exchange Rate Modal -->
    <Transition name="fade">
    <div v-if="showExchange" class="Exchange-overlay" @click.self="toggleExchange">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <h3>환율 계산기</h3>
            <button class="close-button" @click="toggleExchange">&times;</button>
          </div>
          <div class="modal-content">
            <ExchangeView />
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { VueperSlides, VueperSlide } from 'vueperslides'
import 'vueperslides/dist/vueperslides.css'
import ExchangeView from '@/components/ExchangeView.vue'
import { useCounterStore } from '@/stores/counter.js'
import {
  HandHelpingIcon,
  UserIcon,
  CreditCardIcon,
  MapPinIcon,
  Gamepad2Icon,
  DollarSignIcon
} from 'lucide-vue-next'

const router = useRouter()
const showExchange = ref(false)
const store = useCounterStore()

if (!store.allDepositProducts) {
  store.fetchProducts(30)
}

const toggleExchange = () => {
  showExchange.value = !showExchange.value
}

const handleMenuClick = (item) => {
  if (item.route) {
    router.push(item.route)
  } else if (item.type === 'exchange') {
    toggleExchange()
  }
}

const menuItems = ref([
  { 
    icon: CreditCardIcon, 
    label: '예적금 조회', 
    route: { name: 'financialproducts' },
    type: 'route'
  },
  { 
    icon: UserIcon, 
    label: '맞춤형 상품', 
    route: { name: 'recommendedproduct' },
    type: 'route'
  },
  { 
    icon: MapPinIcon, 
    label: '은행찾기', 
    route: { name: 'MapView' },
    type: 'route'
  },
  { 
    icon: Gamepad2Icon, 
    label: '모의주식',    
    route: { name: 'GameView' },
    type: 'route'
  },
  { 
    icon: HandHelpingIcon,
    label: '소통창구',
    route: { name: 'ArticleHomeView' },
    type: 'route'
  },
  {
    icon: DollarSignIcon,
    label: '환율 계산기',
    type: 'exchange'
  },
])

const slides = ref([
  {
    image: '/src/assets/carousel1.png',
  },
  {
    image: '/src/assets/carousel2.png',
  },
  {
    image: '/src/assets/carousel3.png',
    link: '/services/digital'
  }
])

const handleSlideClick = (index) => {
  const slide = slides.value[index]
  if (slide?.link) {
    router.push(slide.link)
  }
}
</script>

<style scoped>

.modal-container {
  background: white;
  width: 400px;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
}

.exchange-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.modal-wrapper {
  position: fixed;
  left: 20px;  /* 왼쪽 여백 */
  bottom: 20px;  /* 아래쪽 여백 */
  z-index: 1001;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #2d71c4;
  color: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.modal-content {
  padding: 20px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  gap: 3rem;
}

.header-text {
  flex: 1;
  min-width: 400px;
}

.main-title {
  font-size: 2.75rem;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: 700;
  white-space: nowrap;
}

.highlight {
  color: #2d71c4;
  font-weight: 800;
}

.sub-title {
  font-size: 1.25rem;
  color: #666;
  font-weight: normal;
  line-height: 1.5;
}

.slider-container {
  width: 500px;
  min-width: 500px;
}

:deep(.vueperslides__track) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

:deep(.vueperslide img) {
  width: 500px;
  height: 300px;
  object-fit: contain;
  object-position: center;
}

.custom-arrow {
  background: rgba(45, 113, 196, 0);
  border: none;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.custom-arrow:hover {
  background: rgba(45, 113, 196, 1);
  transform: scale(1.1);
}

.arrow-icon {
  color: rgb(37, 36, 36);
  font-size: 18px;
  line-height: 1;
}

.products-container {
  background-color: #2d71c4;
  padding: 40px 0;
  width: 100%;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  height: 300px;
  margin: 0;  /* 마진 제거 */
  position: relative;  /* 포지션 추가 */
}

.products-title {
  color: white;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.layout-container {
  display: flex;
  justify-content: space-between; /* space-between으로 변경 */
  gap: 2rem;
  padding: 20px 0;
  align-items: center;
}

.image-container {
  flex: 1; /* 이미지 영역 비율 */
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 300px; /* 이미지 최대 너비 제한 */
}

.banner-image {
  width: 100%;
  height: auto;
  max-height: 200px;
  object-fit: contain;
}

.menu-container {
  display: flex;
  flex: 3; /* 메뉴 영역 비율 증가 */
  gap: 1rem;
  justify-content: flex-start;
  flex-wrap: wrap; /* 필요시 줄바꿈 */
}

.menu-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  transition: transform 0.3s ease;
  padding: 0 10px;
  cursor: pointer;
}

.menu-item:hover {
  transform: translateY(-5px);
}

.icon-container {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.menu-item:hover .icon-container {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.menu-label {
  margin-top: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: white;
  text-align: center;
  white-space: nowrap;
}

.exchange-container {
  position: relative;
  flex: 1;
  min-width: 350px;
  padding: 0;
  border-radius: 12px;
}

.chatbot-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.chatbot-container {
  background: white;
  width: 400px;
  height: 600px;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #2d71c4;
  color: white;
}

.chatbot-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.chatbot-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.close-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 1024px) {
  body {
    overflow-x: auto;
  }

  .header-container {
    min-width: 1200px;
  }

  .products-container {
    min-width: 1200px;
  }

  .menu-container {
    justify-content: space-evenly;
  }

  .layout-container {
    min-width: 1160px;
  }

  .modal-wrapper {
    left: 20px;
    bottom: 20px;
  }
}

@media (max-width: 868px) {
  .header-container {
    flex-direction: row;
    padding: 20px;
  }

  .menu-container {
    flex-wrap: nowrap;
    gap: 1.5rem;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}


</style>