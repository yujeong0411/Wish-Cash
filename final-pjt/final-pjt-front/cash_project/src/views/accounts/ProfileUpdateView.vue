<template>
  <div class="container">
   <header>
     <h1>개인정보 조회/변경</h1>
     <button type="button" @click="signout">회원탈퇴</button>
   </header>

     <div class="form-description">
       <p>고객정보관리 보호를 위해 주요 정보 일부는 ‘*’로 표시됩니다.</p>
       <p>타행이체 불능 시 연락받기 위한 전화번호 변경은 ‘입금불능연락처 변경’ 메뉴를 이용하여 주시기 바랍니다.</p>
       <p>SMS 입출내역통지용 휴대폰 번호 변경은 ‘SMS 입출내역 통지서비스 추가/해지’ 메뉴를 이용하여 주시기 바랍니다.</p>
     </div>
 

   <!-- 언더라인 메뉴 -->
   <ul class="nav nav-underline">
     <li
       v-for="tab in tabs"
       :key="tab.name"
       class="nav-item"
     >
       <a 
         href="#"
         class="nav-link"
         :class="{ active: activeTab === tab.name }"
         @click.prevent="setActiveTab(tab.name)"
       >
         {{ tab.label }}
       </a>
     </li>
   </ul>

   <!-- 콘텐츠 영역 -->
   <div class="tab-content mt-4">
     <div v-if="activeTab === 'profile'">
       <form @submit.prevent="updateProfile">
         <div>
           <label for="nickname">닉네임</label>
           <input type="text" id="nickname" v-model="infoForm.nickname">
         </div>
         <div>
           <label for="email">이메일</label>
           <input type="email" id="email" v-model="infoForm.email">
         </div>
         <div>
           <label for="gender">성별</label>
           <select id="gender" v-model="infoForm.gender">
             <option value="" disabled>성별을 선택하세요.</option>
             <option value="M">남성</option>
             <option value="W">여성</option>
           </select>
         </div>
         <div>
           <label for="birth_date">생년월일</label>
           <input type="date" id="birth_date" v-model="infoForm.birth_date">
         </div>
         <div>
           <label for="house_bank">주거래 은행</label>
           <input type="text" id="house_bank" v-model="infoForm.house_bank" placeholder="은행명을 입력하세요 (예: 신한은행)">
         </div>
         <div class="button-container">
           <button type="button" class="cancel" @click="backProfile">취소</button>
           <button type="submit">변경하기</button>
         </div>
       </form>
     </div>

     <div v-if="activeTab === 'password'">
       <form @submit.prevent="changePassword">
         <div>
           <label for="current-password">현재 비밀번호</label>
           <input id="current-password" v-model="passwordForm.currentPassword" type="password" />
         </div>
         <div>
           <label for="new-password">새 비밀번호</label>
           <input id="new-password" v-model="passwordForm.newPassword" type="password" />
         </div>
         <div>
           <label for="confirm-password">새 비밀번호 확인</label>
           <input id="confirm-password" v-model="passwordForm.confirmPassword" type="password" />
         </div>
         <div class="password-btn">
           <button type="submit">확인</button>
         </div>
       </form>
     </div>
   </div>
 </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import swal from "sweetalert2";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import axios from "axios"

const userStore = useUserStore()
const router = useRouter()
const { userProfile } = storeToRefs(userStore)

// 탭 상태 관리
const activeTab = ref("profile") // 기본 활성화 탭
const tabs = [
 { name: "profile", label: "개인정보 변경" },
 { name: "password", label: "비밀번호 변경" },
]

// 탭 변경 함수
const setActiveTab = (tabName) => {
 activeTab.value = tabName
}

const backProfile = function () {
 router.push({name:'ProfileView'})
}


// 개인정보 변경 폼
const infoForm = ref({
 nickname:'',
 gender:'',
 birth_date:'',
 email:'',
 house_bank:''
})

// 기존 정보 가져오기
onMounted(()=> {
 infoForm.value.nickname = userStore.userProfile.nickname
 infoForm.value.gender = userStore.userProfile.gender
 infoForm.value.birth_date = userStore.userProfile.birth_date
 infoForm.value.email = userStore.userProfile.email
 infoForm.value.house_bank = userStore.userProfile.house_bank
})

// 개인정보 변경 함수 호출
const updateProfile = function () {
 const payload = {...infoForm.value}
 userStore.updateProfile(payload)
}

// 비밀번호 변경 폼
const passwordForm = ref({
 currentPassword: "",
 newPassword: "",
 confirmPassword: "",
})


// 비밀번호는 보안 상 기존 정보를 가져오지 않는다. 
// 비밀번호 변경 함수
const changePassword = function () {
 if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
   swal.fire({ title : "새 비밀번호가 일치하지 않습니다."})
   return
 }
 
 const payload = {
   currentPassword : passwordForm.value.currentPassword,
   newPassword : passwordForm.value.newPassword,
   confirmPassword : passwordForm.value.confirmPassword
 }

 userStore.changePassword(payload)
 .then(() => {
   // 성공 시 폼 초기화
   passwordForm.value.currentPassword = '',
   passwordForm.value.newPassword = '',
   passwordForm.value.confirmPassword = ''
 })
 .catch((err) => {
   console.log(err, "비밀번호 변경 실패")
 })
}

const signout = function() {
  swal.fire({
    title: "회원탈퇴를 진행하시겠습니까?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#2858A6",
    cancelButtonColor: "#828282",
    confirmButtonText: "탈퇴 진행",
    cancelButtonText: "취소",
  }).then((result) => {
    if (result.isConfirmed) {  // selectedDelete 대신 result.isConfirmed 사용
      axios({
        method: "delete",
        url: `http://127.0.0.1:8000/accounts/profile/${userProfile.value.username}/delete/`,
        headers: {
          Authorization: `Token ${userStore.token}`,
        }
      }).then((res) => {
        swal.fire({
          title: "탈퇴 처리되었습니다.",
          icon: "success"
        }).then(() => {
          userStore.logoutUser(); // 확인 버튼 클릭 후 로그아웃
          router.push({ name: "MainView" });
        });
      }).catch((err) => {
        console.log(err);
      });
    } else {
      swal.fire({
        title: "탈퇴를 취소하셨습니다.",
        icon: "info"
      });
    }
  });
}
</script>




<style scoped>
body {
 margin: 0;
 padding: 0;
 width: 100%;
 height: 100%;
 background-color: #f4f6f8; /* 연한 회색 배경 */
}

.container {
 width: 100%;
 max-width: 1200px;
 margin: 0 auto; /* 페이지 중앙 정렬 */
 padding: 20px;
 background-color: #ffffff; /* 하얀 배경 */
 box-sizing: border-box;
}

/* 헤더 스타일 */
header {
 display: flex;
 justify-content: space-between; /* 회원탈퇴 버튼을 오른쪽으로 */
 align-items: center;
 border-bottom: 2px solid #ececec; /* 얇은 경계선 */
 padding-bottom: 10px;
 margin-bottom: 20px;
}

header h1 {
 font-size: 32px;
 font-weight: bold;
 color: #0f0c0c; /* 파란색 */
 margin: 0;
}

header button {
 padding: 6px 12px;
 font-size: 14px;
 color: rgb(253, 253, 253);
 background-color: #f33737; /* 회원탈퇴는 빨간 버튼 */
 border: none;
 border-radius: 4px;
 cursor: pointer;
}

header button:hover {
 background-color: #d32f2f; /* 호버 시 더 어두운 빨간색 */
}

/* 설명 텍스트 스타일 */
.form-description {
 padding: 10px 0;
 margin-bottom: 20px;
 line-height: 1.6; /* 줄 간격 */
}

.form-description p {
 font-size: 14px;
 color: #666; /* 어두운 회색 텍스트 */
 margin: 5px 0;
}

/* 언더라인 메뉴 스타일 */
.nav-underline {
 display: flex;
 list-style: none;
 padding: 0;
 margin: 0;
}

.nav-item {
 margin-right: 20px;
}

.nav-link {
 text-decoration: none;
 font-size: 16px;
 color: #747577;
 padding: 8px 0;
 transition: color 0.3s ease, border-bottom 0.3s ease;
}

.nav-link.active {
 color: #2858a6; /* 파란색 */
 font-weight: bold;
 border-bottom: 2px solid #2858a6;
}

.nav-link:hover {
 color: #003c82; /* 호버 시 더 어두운 파란색 */
}

/* 폼 스타일 */
form {
 width: 100%; /* 폼이 부모 요소의 전체 너비를 차지 */
 display: flex;
 flex-direction: column; /* 세로로 배치 */
 gap: 12px; /* 각 필드 사이 간격 */
 margin-top: 20px;
}

form div {
 display: flex; /* 라벨과 입력 필드를 한 줄로 배치 */
 flex-direction: column; /* 라벨 위, 입력 필드 아래 */
 gap: 2px; /* 라벨과 입력 필드 간격 최소화 */
}

form label {
 font-size: 14px;
 color: #333; /* 어두운 회색 */
 margin-bottom: 0px; /* 라벨과 입력 필드 사이 간격 최소화 */
}

form input,
form select {
 padding: 12px; /* 입력 필드 패딩 */
 font-size: 14px;
 border: 1px solid #ddd;
 border-radius: 4px;
 box-sizing: border-box;
 width: 100%;
 background-color: #f9f9f9; /* 입력 필드의 연한 배경 */
}

.password-btn, .button-container {
 display: flex;
 flex-direction: row;
 justify-content: center; /* 버튼을 중앙 정렬 */
 gap: 15px; /* 버튼 간격 */
 margin-top: 20px; /* 버튼과 입력 필드 간격 */
}

form button {
 flex: 1; /* 버튼이 동일한 비율로 공간을 차지 */
 max-width: 150px; /* 버튼의 최대 크기 제한 */
 padding: 8px 12px; /* 버튼 내부 여백 */
 font-size: 14px;
 color: white;
 background-color: #2d71c4; /* 파란색 버튼 */
 border: none;
 border-radius: 4px;
 cursor: pointer;
 transition: background-color 0.3s ease;
 text-align: center; /* 텍스트 중앙 정렬 */
}

form button:hover {
  background-color: #003c82;
}

form button.cancel {
 background-color: #ddd; /* 취소 버튼은 회색 */
 color: #333; /* 어두운 회색 텍스트 */
}

form button.cancel:hover {
 background-color: #bbb; /* 호버 시 더 어두운 회색 */
}

form .confirm-button {
 padding: 6px 12px; /* 확인 버튼 크기 축소 */
}

</style>
