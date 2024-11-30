<template>
  <div class="login-container">
    <!-- 타이틀 -->
    <header class="header">
      <h1>로그인</h1>
    </header>
    
    <section class="form-description">
      <div class="description-content">
        <!-- 이미지 -->
        <div class="form-image">
          <img src="@/assets/보안아이콘.png" alt="보안아이콘" />
        </div>

        <!-- 텍스트 -->
        <div class="form-text">
          <p><strong class="highlight">아직 계정이 없으신가요? 지금 가입하세요!</strong></p>
          <p class="small-text">최고의 보안 기술로 고객의 정보를 안전하게 보호합니다.</p>
          <p class="small-text">수사기관 등 공공기관은 어떤 명목으로도 통장 비밀번호 등 금융정보를 묻거나 범죄에 연루되었다는 등의 이유로 돈을 요구하지 않습니다.</p>
        </div>
      </div>
    </section>

    <!-- 이미지와 로그인 폼을 담는 행 -->
    <div class="content-row">
      <!-- 이미지 -->
      <div class="image-container">
        <img src="@/assets/login.png" alt="login" />
      </div>

      <!-- 로그인 폼 -->
      <section class="login-form-container">
        <form @submit.prevent="loginForm" class="login-form">
          <div class="form-row">
            <!-- 입력 필드 -->
            <div class="form-fields">
              <div class="form-group">
                <input
                  type="text"
                  id="username"
                  v-model="state.username"
                  placeholder="사용자ID"
                  class="form-input"
                  @blur="v$.username.$touch"
                />
                <span v-if="v$.username.$error" class="error-message">아이디가 틀렸습니다.</span>
              </div>

              <div class="form-group password-group">
                <div class="password-input-container">
                  <input
                    :type="visible ? 'text' : 'password'"
                    id="password"
                    v-model="state.password"
                    placeholder="비밀번호"
                    class="form-input"
                    @blur="v$.password.$touch"
                  />
                  <button type="button" class="toggle-visibility" @click="visible = !visible">
                    {{ visible ? "숨기기" : "보기" }}
                  </button>
                </div>
                <span v-if="v$.password.$error" class="error-message">비밀번호가 틀렸습니다.</span>
              </div>
            </div>

            <!-- 버튼 -->
            <div class="form-buttons">
              <button type="submit" class="login-button">로그인</button>
              <button type="button" class="signup-button" @click="goToSignup">회원가입</button>
            </div>
          </div>
        </form>
      </section>
    </div>
    <hr class="divider">
  </div>
</template>


<script setup>
import { ref } from 'vue';
import useVuelidate from '@vuelidate/core';
import { required, minLength, maxLength, minValue } from '@vuelidate/validators';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
import SignUpView from './SignUpView.vue';

const router = useRouter()
const visible = ref(false)
const userstore = useUserStore()
const state = ref({
  username:'',
  password:''
})

// 유효성 검사
const rules = {
  username: {required, minLength:minLength(5), maxLength: maxLength(20)},
  password: {required, minLength : minLength(8), maxLength : maxLength(20)}
}

const v$ = useVuelidate(rules, state)

const loginForm = function () {
  v$.value.$validate()
  if (!v$.value.$error) {
    // 유효성 검사를 통과 했다면 
    const payload = {
      username : state.value.username,
      password : state.value.password
    }
    console.log("Payload 확인:", payload)
    userstore.loginUser(payload)
  } else {
    alert("입력한 정보를 확인해주세요.")
  }
}

// 회원가입 페이지 이동 
const goToSignup = function () {
  router.push({name:'SignUpView'})
}
</script>



<style scoped>
/* 전체 컨테이너 */
.login-container {
  width: 100%;
  min-width: 800px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #ffffff;
  box-sizing: border-box;
  font-family: 'Noto Sans KR', sans-serif;
}

/* 타이틀 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  position: relative;
}

.header::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(to right, #91919f, #8caff5);
}

h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111111;
  margin: 0;
  letter-spacing: -0.5px;
}

/* 설명 박스 */
.form-description {
  background: linear-gradient(145deg, #f8f9fd 0%, #f2f4f8 100%);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
}

.description-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.form-image {
  flex-shrink: 0;
}

.form-image img {
  width: 80px;
  height: auto;
}

.form-text {
  flex: 1;
}

.highlight {
  color: #111111;
  font-size: 16px;
  margin-bottom: 10px;
}

.small-text {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 8px 0;
}

/* 콘텐츠 영역 */
.content-row {
  display: flex;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  width: 100%;
  margin: 40px 0;
}

.image-container {
  flex: 1;
  max-width: 400px;
}

.image-container img {
  width: 100%;
  height: auto;
  border-radius: 12px;
}

/* 로그인 폼 */
.login-form-container {
  min-width: 400px;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 380px;
  padding: 15px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #0046FF;
  box-shadow: 0 0 0 3px rgba(0, 70, 255, 0.1);
}

.password-input-container {
  position: relative;
}

.toggle-visibility {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #2d71c4;
  cursor: pointer;
  font-size: 14px;
}

/* 버튼 */
.form-buttons {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}

.login-button,
.signup-button {
  width: 190px;
  padding: 14px 0;
  font-size: 16px;
  font-weight: 500;
  color: white;
  background-color: #8595a9;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover,
.signup-button:hover {
  background-color: #0173ba;
}

/* 구분선 */
.divider {
  border: 0;
  height: 1px;
  background: #d2d2d2;
  margin: 30px 0;
}

/* 에러 메시지 */
.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-top: 5px;
}

/* 반응형 */
@media (max-width: 900px) {
  .login-container {
    min-width: 800px;
  }

  .content-row {
    gap: 20px;
  }

  .image-container {
    max-width: 300px;
  }
}
</style>


