<script setup>
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import { ref, onMounted, computed, watch} from "vue";
import { useUserStore } from '@/stores/user';
import { useCounterStore } from '@/stores/counter'
import Swal from 'sweetalert2'
import { storeToRefs } from "pinia";
import ChatbotView from '@/components/Chatbot.vue'
import { BotIcon } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const store = useCounterStore()
const { isLogin } = storeToRefs(userStore);

// `isMainView`를 반응형으로 설정
const isMainView = computed(() => route.name === 'MainView');

const showChatbot = ref(false)

const toggleChatbot = () => {
  showChatbot.value = !showChatbot.value
}

const logout = function () {
  Swal.fire({
    title: "정말 로그아웃 하시겠습니까?",
    text: "로그아웃 후 다시 로그인 하실 수 있습니다.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#2858A6",
    cancelButtonColor: "#828282",
    confirmButtonText: "로그아웃",
    cancelButtonText: "취소",
  }).then((result) => {
    console.log(result, "로그아웃 res")
    if (result.isConfirmed) {
      userStore.logoutUser()
    } else {
      Swal.fire({
        title: "로그아웃이 취소되었습니다."
      })
    }
  })
}


onMounted(async () => {
  await store.saveDepositProducts();
  await store.saveSavingProducts();
})


</script>


<template>
  <div id="app" class="app">
    <!-- MainView 전용 헤더 -->
    <header v-if="isMainView" class="header-main">
      <div class="header-row">
          <RouterLink :to="{ name: 'MainView' }" class="header-logo">
            <img src="@/assets/wishcash-logo.png" alt="wishcash_logo" class="logo">
            <h1>WISH CASH</h1>
          </RouterLink>
        <div class="nav-right">
          <div v-if="isLogin" class="nav-right-links">
            <p class="username"><strong>{{ userStore.userInfo.username }}</strong> 님</p>
            <RouterLink :to="{name:'ProfileView'}">마이페이지</RouterLink>   
            <button @click="logout" class="logout-btn">로그아웃</button>
          </div>
          <div v-else class="login-signup-links">
            <RouterLink :to="{name:'LoginView'}">로그인</RouterLink> 
            <RouterLink :to="{name:'SignUpView'}">회원가입</RouterLink>
          </div>
          <button class="chatbot-button" @click="toggleChatbot">
            <BotIcon size="30"></BotIcon>
          </button>
        </div>
      </div>
    </header>

    <!-- 다른 페이지 헤더 -->
    <header v-else class="header-default">
      <div class="header-row">
        <RouterLink :to="{ name: 'MainView' }" class="header-logo">
          <img src="@/assets/wishcash-logo.png" alt="wishcash_logo" class="logo">
          <h1>WISH CASH</h1>
        </RouterLink>
        <div class="nav-right">
          <div v-if="isLogin" class="nav-right-links">
            <RouterLink v-if="userStore.userInfo" :to="{ name: 'ProfileView' }" class="user-link">
            </RouterLink>
            <p class="username"><strong>{{ userStore.userInfo.username }}</strong> 님</p>
            <RouterLink :to="{name:'ProfileView'}">마이페이지</RouterLink>   
            <button @click="logout" class="logout-btn">로그아웃</button>
          </div>
          <div v-else class="login-signup-links">
            <RouterLink :to="{name:'LoginView'}">로그인</RouterLink> 
            <RouterLink :to="{name:'SignUpView'}">회원가입</RouterLink>
          </div>
          <button class="chatbot-button" @click="toggleChatbot">
            <BotIcon size="30"></BotIcon>
          </button>
        </div>
      </div>
      <!-- 중앙 메뉴 -->
      <nav class="nav-center">
        <RouterLink :to="{name:'financialproducts'}">예적금 조회</RouterLink>
        <RouterLink :to="{name:'recommendedproduct'}">맞춤형 상품</RouterLink>
        <RouterLink :to="{name:'MapView'}">주변 은행찾기</RouterLink>
        <RouterLink :to="{name:'GameView'}">모의 주식</RouterLink>
        <RouterLink :to="{name:'ArticleHomeView'}">소통 창구</RouterLink>   <!-- 수정 필요 -->
      </nav>
    </header>

    <main>
      <RouterView />
    </main>

    <footer class="footer">
    <div class="footer-container">
        <div class="footer-info">
          <p class="address">광주광역시 광산구 소망로 123, WishCash 빌딩</p>
          <div class="contact-info">
            <p>Tel: 02-123-4567</p>
            <span class="divider">|</span>
            <p>Email: choiyujeong0411@wishcash.com</p>
          </div>
        </div>
      <div class="footer-links">
        <RouterLink :to="{ name: 'MainView' }">홈</RouterLink>
        <RouterLink :to="{ name: 'financialproducts' }">예적금 조회</RouterLink>
        <RouterLink :to="{ name: 'recommendedproduct' }">맞춤형 상품</RouterLink>
        <RouterLink :to="{ name: 'ArticleHomeView' }">소통창구</RouterLink>
        <RouterLink :to="{ name: 'ProfileView' }">마이 페이지</RouterLink>
      </div>
      <div class="footer-bottom">
        <p>© 2024 Wish Cash. 모든 권리 보유.</p>
      </div>
    </div>
  </footer>
</div>

  <!-- Chatbot Modal -->
  <Transition name="fade">
      <div v-if="showChatbot" class="chatbot-overlay" @click.self="toggleChatbot">
        <div class="chatbot-container">
          <div class="chatbot-header">
            <h3>Wish Cash 챗봇</h3>
            <button class="close-button" @click="toggleChatbot">&times;</button>
          </div>
          <div class="chatbot-content">
            <ChatbotView />
          </div>
        </div>
      </div>
    </Transition>
</template>




<style scoped>
.app {
  position: relative;
  min-height: 100vh;
  min-width: 1024px; /* 최소 너비 설정 */
  display: flex;
  flex-direction: column; /* 세로 방향으로 레이아웃 설정 */
}

main {
  flex-grow: 1; /* main 영역이 남은 공간을 차지하도록 설정 */
}

.nav-container {
  display: flex;
  justify-content: flex-end;
  padding: 10px 20px;
  background-color: #ffffff;
  min-width: 800px;
  border-bottom: 1px solid #eee;
  
}

.user-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-link {
  color: #333;
  text-decoration: none;
  font-size: 14px;
  display: flex;
  align-items: center;
}

strong {
  color:#0173BA
}

.username {
  color: #000000;
  margin-right: 2px;
}

.nav-link {
  color: #666;
  font-size: 14px;
  text-decoration: none;
  transition: color 0.2s ease;
}

.login-signup-links {
  display: flex;
  gap: 15px; /* 링크 사이의 간격 */
  align-items: center;
}


/* 공통 헤더 스타일 */
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #ffffff;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none; /* 링크 밑줄 제거 */
}

.header-logo h1 {
  font-size: 30px;
  font-weight: 600;
  color: rgb(0, 0, 0);
  margin: 0;
  padding-left: 10px;
}

/* header-default에도 최소 너비 적용 */
.header-default {
  width: 100%;
  min-width: 1024px; /* app과 동일한 최소 너비 */
  box-sizing: border-box;
}

/* 로고 이미지 스타일 */
.logo {
  width: 40px;
  height: 40px;
  border-radius: 50%; /* 로고를 둥글게 */
  object-fit: cover;
}

/* 오른쪽 메뉴 스타일 */
.nav-right {
  display: flex;
  align-items: center;
}

.nav-right a,
.nav-right button {
  color: rgb(0, 0, 0);
  text-decoration: none;
  font-size: 16px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: color 0.3s ease;
}

.nav-right a:hover,
.nav-right button:hover {
  color:#0173BA;
}

/* nav-center도 최소 너비 설정 */
.nav-center {
  display: flex;
  justify-content: center;
  gap: 50px;
  background-color: #0173BA;
  padding: 10px 0;
  white-space: nowrap;
  width: 100%;
  min-width: 1024px; /* app과 동일한 최소 너비 */
  box-sizing: border-box;
  overflow-x: hidden; /* nav 자체의 스크롤은 방지 */
}

.nav-center a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
}

.nav-center a:hover {
  text-decoration: underline;
}

.nav-right-links {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-link,
.nav-link,
.logout-btn {
  color: rgb(0, 0, 0);
  text-decoration: none;
  font-size: 13px;
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
  transition: color 0.3s ease;
  white-space: nowrap; /* 줄바꿈 방지 */
}

.footer {
  width: 100%;
  background-color: #ffffff;
  color: #333333;
  padding: 10px 20px;
  margin-top: 0;
  border-top: 1px solid #eaeaea;
  box-sizing: border-box;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}


.address {
  color: #666666;
  margin-bottom: 0px;
  font-size: 13px;
}

.contact-info {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  color: #666666;
  font-size: 13px;
  margin-bottom: 0px;
}

.divider {
  color: #eaeaea;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 7px;
}

.footer-links a {
  color: #666666;
  text-decoration: none;
  font-size: 13px;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #0173BA;
}

.footer-bottom {
  text-align: center;
  padding-top: 2px;
  color: #999999;
  font-size: 11px;
}

/* 챗봇 버튼 스타일 */
.chatbot-button {
  background-color: #0173BA;
  color: white;
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 20px;
  transition: background-color 0.3s;
}

.chatbot-button:hover {
  background-color: #015f8d;
}

/* 챗봇 모달 오버레이 스타일 */
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
  z-index: 10; /* 챗봇이 다른 요소들 위에 표시되도록 */
}

.chatbot-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 추가 */
}


.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatbot-content {
  margin-top: 10px;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #333;
}
</style>

