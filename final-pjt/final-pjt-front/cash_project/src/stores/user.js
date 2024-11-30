import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import swal from 'sweetalert2'
import axios from 'axios'



export const useUserStore = defineStore('user', () => {
  const API_URL = "http://127.0.0.1:8000"
  const router = useRouter()
  const token = ref(null)
  const userInfo = ref(null)  // 로그인 시 제공된 기본정보
  const userProfile = ref(null)   // 로그인 이후 추가적 정보
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

   // 회원가입
   const createUser = function (payload) {
    const { realname, username, password1, password2, age, gender, birth_date, email, house_bank, nickname } = payload
    console.log("Payload 확인:", {
      realname,
      nickname,
      username, 
      password1, 
      password2, 
      age, 
      gender, 
      birth_date, 
      email, 
      house_bank
    });
    axios ({
      method : 'post',
      url : `${API_URL}/dj-rest-auth/registration/`,
      data : {
        realname,
        nickname,
        username, 
        password1, 
        password2, 
        age, 
        gender, 
        birth_date, 
        email, 
        house_bank
      }
    }).then((res) => {
      console.log(res)
      const password = password1
      const payload = {
        username,
        password
      }
      loginUser(payload)   // 회원가입 성공 후 로그인 함수 호출
    }).catch((err) => {
      console.log(err)
      if (err.response.data) {
        const errors = err.response.data
        if (errors.username) {
          swal.fire({
            text:errors.username[0],
            icon:"error"
          })
        } else {
          swal.fire("다시 입력 정보를 확인해주세요.")
        }
      }
    })
  }

  // 로그인 
  const loginUser = function(payload) {
    const { username, password } = payload
    axios({
      method:'post',
      url:`${API_URL}/dj-rest-auth/login/`,
      data:{
        username,
        password
      }
    }).then((res) => {
      console.log(res.data, "로그인 성공")
      token.value = res.data.key
      userInfo.value = res.data.user
      router.push({name:'ProfileView'})
      swal.fire({
        title: `${res.data.user.username}님, 환영합니다.`,
        icon: 'success',
        timer: 1000,    // 1초
        showConfirmButton: false // 확인 버튼 제거 
      })
    }).catch((err) => {
      console.log(err.response)
      swal.fire({
        title: '오류 발생',
        text: '입력 정보를 다시 확인해주세요.',
        icon: 'error', // 에러 메시지 아이콘
      })
    })
  }



  // 로그아웃 
  const logoutUser = function () {
    axios({
      method:'post',
      url:`${API_URL}/dj-rest-auth/logout/`,
    }).then((res) => {
      console.log(res)
      token.value = null
      userInfo.value = null
      userProfile.value = null
      swal.fire("로그아웃 되었습니다.", "다음에 또 만나요!", "success");
      router.push({ name: "MainView" })
    }).catch((err) => {
      console.log(err)
    })
  }


  // 프로필
  const getProfile = function () {
    console.log(userInfo.value, "프로필")
    if (!userInfo.value) {
      console.log("유저정보가 없습니다.")
      return
    }
    axios({
      method:'get',
      url: `${API_URL}/accounts/profile/${userInfo.value.username}/`,
      headers: {
        Authorization:`Token ${token.value}`
      }
    }).then((res) => {
      console.log(res.data, "프로필 성공")
      userProfile.value = res.data
    }).catch((err) => {
      console.log(err, "프로필 에러")
    })
  }
  

  // 프로필 수정
  const updateProfile = function (payload) {
    console.log("프로필 수정")
    axios.put(`${API_URL}/accounts/profile/${userInfo.value.username}/`, 
      payload,
      {
        headers : {
          Authorization: `Token ${token.value}`
        }
      }).then((res) => {
        userProfile.value = {...userProfile.value, ...payload}
        swal.fire({
          title: '변경되었습니다.',
          timer: 1000
        })
      }).catch((err) => {
        console.log(err)
        swal.fire({
          title: "변경에 실패했습니다. 정보를 다시 확인하세요.",
          timer: 1000
        })
      })
  }

  // 비밀번호 수정
  const changePassword = function (payload) {
    const errorMessages = {
      'This password is too short. It must contain at least 8 characters.': '비밀번호는 최소 8자 이상이어야 합니다.',
      'This password is too common.': '이 비밀번호는 너무 일반적입니다. 다른 비밀번호를 설정해주세요.',
      'This password is entirely numeric.': '비밀번호는 숫자로만 구성될 수 없습니다.',
      'The password is too similar to the username.': '비밀번호가 아이디와 너무 유사합니다.',
      'Your old password was entered incorrectly. Please enter it again.': '현재 비밀번호가 올바르지 않습니다. 다시 입력해주세요.',
      'The two password fields didn\'t match.': '새 비밀번호가 일치하지 않습니다.',
      'This password is too similar to your other personal information.': '비밀번호가 개인정보와 너무 유사합니다.',
    }

    return axios.post(
      `${API_URL}/dj-rest-auth/password/change/`, 
      {
        old_password: payload.currentPassword,
        new_password1: payload.newPassword,
        new_password2: payload.confirmPassword
      },
      {
        headers: {
          Authorization: `Token ${token.value}`
        }
      }
    ).then((res) => {
      console.log('비밀번호 변경 성공:', res)
      swal.fire({
        title: "비밀번호가 변경되었습니다.",
        icon: 'success',
        timer: 1500
      })
      return res
    }).catch((err) => {
      console.log('비밀번호 변경 에러:', err.response?.data)
      
      // 에러 메시지 처리
      let errorMessage = "비밀번호 변경에 실패했습니다."
      
      if (err.response?.data) {
        const errorData = err.response.data;
        
        // 현재 비밀번호 오류
        if (errorData.old_password) {
          const englishMessage = errorData.old_password[0];
          errorMessage = errorMessages[englishMessage] || englishMessage;
        }
       // 새 비밀번호 오류
      else if (errorData.new_password1) {
        if (Array.isArray(errorData.new_password1)) {
          // 각 에러 메시지를 한글로 변환
          errorMessage = errorData.new_password1
            .map(msg => errorMessages[msg] || msg)
            .join('\n');
        } else {
          errorMessage = errorMessages[errorData.new_password1] || errorData.new_password1;
        }
      }
      // 새 비밀번호 확인 오류
      else if (errorData.new_password2) {
        const englishMessage = errorData.new_password2[0];
        errorMessage = errorMessages[englishMessage] || englishMessage;
      }
      // 비밀번호 불일치
      else if (errorData.non_field_errors) {
        const englishMessage = errorData.non_field_errors[0];
        errorMessage = errorMessages[englishMessage] || englishMessage;
      }
    }

    swal.fire({
      title: '비밀번호 변경 실패',
      html: errorMessage.replace(/\n/g, '<br>'),
      icon: 'error',
      confirmButtonColor: '#2858A6'
    })
    throw err
  })
}

  return { 
    createUser, 
    loginUser, 
    getProfile, 
    token, 
    isLogin, 
    userInfo, 
    userProfile, 
    logoutUser,
    updateProfile,
    changePassword
  }
}, {persist:true})
