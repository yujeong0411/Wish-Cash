<template>
  <div class="signup-container">
   <!-- 타이틀 -->
   <header class="header">
     <h1>회원가입</h1>
   </header>

   <section class="form-description">
     <p class="description-1"><strong><span class="highlight">WISH CASH</span>에 오신 것을 환영합니다.</strong></p>
     <p class="description-2">WISH CASH 홈페이지 회원(14세 이상)으로 가입하시면 환율계산, 이벤트 참여, 금융상품 조회 등 다양한 서비스를 이용하실 수 있습니다.</p>
   </section>
 
 <section class="terms-section">
   <div class="form-check-container">
     <div class="form-check">
       <div class="terms-container">
         <p><strong class="highlight">회원 서비스 이용약관</strong></p>
         <p class="terms-description">홈페이지 회원 서비스 이용약관에 동의하십니까?</p>
         <div class="terms-agree">
           <input type="checkbox" id="service" value="service" v-model="selected" class="form-check-input" />
           <label for="service" class="form-check-label">예, 동의합니다.</label>
         </div>
       </div>
     </div>
 
     <div class="form-check">
       <div class="terms-container">
         <p><strong class="highlight">개인정보 수집 및 이용 동의서</strong></p>
         <p class="terms-description">홈페이지 회원 개인정보 수집 및 이용 동의서를 확인하고 개인정보 수집 및 이용에 동의하십니까?</p>
         <div class="terms-agree">
           <input type="checkbox" id="info" value="info" v-model="selected" class="form-check-input" />
           <label for="info" class="form-check-label">예, 동의합니다.</label>
         </div>
       </div>
     </div>
   </div>
 </section>
 
 
 
 <section class="signup-form">
   <form @submit.prevent="signupForm">
     <div class="form-row">
       <div class="form-group">
         <label for="username">*아이디</label>
         <input 
           id="username" 
           type="text" 
           v-model="state.username" 
           @blur="v$.username.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.username.$error">아이디는 5~20글자입니다.</span>
       </div>
     
       <div class="form-group">
         <label for="realname">*이름</label>
         <input 
           id="realname" 
           type="text" 
           v-model="state.realname" 
           @blur="v$.realname.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.realname.$error">이름에는 숫자나 특수 문자를 사용할 수 없습니다.</span>
       </div>
     </div>
 
     <div class="form-row">
       <div class="form-group">
         <label for="nickname">닉네임</label>
         <input 
           id="nickname" 
           type="text" 
           v-model="state.nickname" 
           @blur="v$.nickname.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.nickname.$error">닉네임은 최대 10글자입니다.</span>
       </div>
 
       <div class="form-group">
         <label for="email">이메일</label>
         <input 
           id="email" 
           type="text" 
           v-model="state.email" 
           @blur="v$.email.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.email.$error && v$.email.$dirty">올바른 이메일 형식이 아닙니다. 예: example@domain.com</span>
       </div>
     </div>
 
     <div class="form-row">
       <div class="form-group">
         <label for="password1">*비밀번호</label>
         <input 
           id="password1" 
           type="password" 
           v-model="state.password1" 
           @blur="v$.password1.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.password1.$error">비밀번호는 8~20자로 입력하세요.</span>
       </div>

       <div class="form-group">
         <label for="password2">*비밀번호 확인</label>
         <input 
           id="password2" 
           type="password" 
           placeholder="비밀번호를 다시 입력하세요." 
           v-model="state.password2" 
           @blur="v$.password2.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.password2.$error">비밀번호가 일치하지 않습니다.</span>
       </div>
     </div>
 
     <div class="form-row">
       <div class="form-group">
         <label for="age">*나이</label>
         <input 
           id="age" 
           type="number" 
           v-model="state.age" 
           @blur="v$.age.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.age.$error">가입 가능한 나이는 18세에서 99세입니다.</span>
       </div>
 
       <div class="form-group">
         <label for="gender">*성별</label>
         <select 
           id="gender" 
           v-model="state.gender" 
           @blur="v$.gender.$touch" 
           class="form-input"
         >
           <option value="" disabled>성별을 선택하세요.</option>
           <option value="M">남성</option>
           <option value="W">여성</option>
         </select>
         <span class="error-message" v-if="v$.gender.$error">성별을 선택해주세요.</span>
       </div>
     </div>
 
     <div class="form-row">
       <div class="form-group">
         <label for="house_bank">주거래 은행</label>
         <input 
           id="house_bank" 
           type="text" 
           v-model="state.house_bank" 
           placeholder="은행명을 입력하세요 (예: 신한은행)" 
           @blur="v$.house_bank.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.house_bank.$error">주거래 은행은 한 개만 입력 가능합니다.</span>
       </div>
 
       <div class="form-group">
         <label for="birth_date">*생년월일</label>
         <input 
           id="birth_date" 
           type="date" 
           v-model="state.birth_date" 
           @blur="v$.birth_date.$touch" 
           class="form-input"
         />
         <span class="error-message" v-if="v$.birth_date.$error">생년월일을 입력하세요.</span>
       </div>
     </div>
 
     <button type="submit" class="submit-button">가입하기</button>
   </form>
 </section>
</div>
 </template>
 
 
 
 <script setup>
 import { ref, computed } from 'vue';
 import useVuelidate from "@vuelidate/core";   // 유효성 검증
 import { required, minLength, maxLength, minValue, maxValue, sameAs, email, helpers } from "@vuelidate/validators"
 import { useUserStore } from '@/stores/user';
 import swal from 'sweetalert2'


 const selected = ref([])   // 약관 동의 상태 
 const userstore = useUserStore()
 
 // 데이터 저장
 const state = ref({
   realname : null,
   username : null,
   nickname : null,
   email : '',
   password1 : '',
   password2: '',
   age : null,
   gender : null,
   birth_date: null,
   house_bank : ''
 })

 const noSpecialChars = helpers.withMessage(
   "특수 문자는 허용되지 않습니다.",
   (value) => {
     return /^[a-zA-Z가-힣\s]+$/.test(value);
   }
 );

 
 // 유효성 검증 규칙
 const rules = computed(() => ({
   username: {required, minLength:minLength(5), maxLength:maxLength(20)},
   realname: {required, noSpecialChars},
   nickname: {maxLength : maxLength(10)},
   password1: {required, minLength : minLength(8), maxLength : maxLength(20)},
   password2: {required, sameAs : sameAs(computed(()=>state.value.password1))},
   gender: {required},
   age: {required, minValue : minValue(18), maxValue: maxValue(99)},
   email: {email},
   birth_date: {required},
   house_bank: {maxLength: maxLength(10)},
 
 }))
 
 // 유효성 검증 
 const v$ = useVuelidate(rules, state)
 
 const signupForm = function() {
   console.log("signupForm 함수 호출됨")
   v$.value.$validate()   // 유효성 검사
   if (selected.value.length !== 2) {
     swal.fire("모든 약관에 동의 해야합니다.")
     return router.push({ name: "SignupView" })
   }
   else if (selected.value.length == 2 && !v$.value.$error) {   // 유효성 검사를 모두 통과했을 경우
     const payload = {     // 전송할 데이터 
       realname : state.value.realname,
       username: state.value.username,
       nickname: state.value.nickname,
       password1: state.value.password1,
       password2: state.value.password2,
       age: state.value.age,
       gender: state.value.gender,
       email: state.value.email,
       birth_date: state.value.birth_date,
       house_bank: state.value.house_bank
     }
     console.log("signupForm 가입")
     userstore.createUser(payload)
   } else {
     swal.fire("* 표시가 된 칸은 필수 입력입니다.")
   }
 }
 </script>
 
 
 
 <style scoped>
 /* 전체 컨테이너 */
 .signup-container {
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
   text-align: left; /* 왼쪽 정렬 */
 }
 
 .description-1 {
   font-size: 18px;
   color: #333;
 }
 
 .description-1 .highlight {
   color: #2858A6; /* WISH CASH 강조 색상 */
 }
 
 .description-2 {
   font-size: 14px;
   color: rgb(83, 80, 80);
 }
 
 /* 구분선 */
 .divider {
   border: none;
   border-top: 1px solid #28347B;
   width: 80%;
   max-width: 1200px;
   margin: 20px auto;
 }
 
 /* 회원가입 폼 */
 .signup-form {
   width: 80%;
   max-width: 1200px;
   margin: 30px auto;
   padding-bottom: 30px;
   text-align: center;
 }
 
 .form-row {
   display: flex;
   justify-content: space-between;
   margin-bottom: 25px;
 }
 
 .form-group {
   width: 48%;
   display: flex;
   flex-direction: column;
   align-items: flex-start;
 }
 
 .form-group label {
   font-weight: bold;
   margin-bottom: 10px;
   display: block;
   font-size: 16px;
 }
 
 .form-input {
   width: 100%;
   padding: 10px;
   border: 1px solid #dcdcdc;
   border-radius: 4px;
   box-sizing: border-box;
   font-size: 16px;
 }
 
 .form-input:focus {
   outline: none;
   border-color: #2858A6;
   box-shadow: 0px 0px 5px rgba(0, 114, 206, 0.5);
 }
 
 .error-message {
   color: #ff4d4f;
   font-size: 13px;
   margin-top: 5px;
 }
 
 .submit-button {
   width: 180px;
   padding: 13px;
   background-color: #2858A6;
   color: #ffffff;
   font-size: 18px;
   font-weight: bold;
   border: none;
   border-radius: 4px;
   cursor: pointer;
   transition: background-color 0.3s;
 }
 
 .submit-button:hover {
   background-color: #042b52;
 }
 
 /* 약관 섹션 */
 .terms-section {
   width: 80%;
   max-width: 1000px;
   margin: 40px auto;
   padding: 20px;
   box-sizing: border-box;
 }
 
 .form-check-container {
   display: flex;
   justify-content: space-between;
   gap: 20px;
   flex-wrap: wrap;
   width: 100%;
   box-sizing: border-box;
 }
 
 .form-check {
   flex: 1;
   max-width: 48%;
   padding: 16px;
   border: 1px solid #000000;
   box-sizing: border-box;
   position: relative;
 }
 
 .terms-container {
   display: flex;
   flex-direction: column;
   align-items: flex-start;
 }
 
 .terms-description {
   font-size: 14px;
   color: #897E7E;
   margin-bottom: 40px;
   word-break: break-word;
 }
 
 .terms-agree {
   display: flex;
   align-items: center;
   position: absolute;
   right: 15px;
   bottom: 15px;
 }
 
 .form-check-input {
   margin-right: 10px;
   width: 18px;
   height: 18px;
   border: 1px solid #000000;
 }
 
 .form-check-label {
   font-size: 13px;
   font-weight: 400;
 }
 
 /* 기본 컨테이너들의 최소 너비 설정 */
 .header,
 .form-description,
 .terms-section,
 .signup-form {
   min-width: 850px; /* body의 min-width보다 약간 작게 설정 */
 }
 
 body {
   min-width: 900px; /* 화면 크기가 최소 900px로 유지되도록 설정 */
   overflow-x: auto; /* 화면이 작아지면 수평 스크롤바 활성화 */
 }
 </style>