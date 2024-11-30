<template>
  <div class="registration-container">
    <h1>상품 가입 신청</h1>

    <!-- 약관 -->
    <div class="terms-section block">
      <h2>은행 약관</h2>
      <div class="terms-box">
        <p>1. 본 신청서를 제출함으로써 귀하는 상품 가입 약관에 동의하게 됩니다.</p>
        <p>2. 은행은 귀하의 개인정보를 상품 가입과 관리를 위한 목적으로만 사용합니다.</p>
        <p>3. 가입한 상품은 관련 법규에 따라 보호되며, 은행 정책에 따라 운영됩니다.</p>
        <p>4. 상품 해지나 조건 변경은 반드시 은행과 협의 후 진행되어야 합니다.</p>
        <p>5. 귀하의 계좌는 은행의 보안 정책에 따라 안전하게 보호됩니다.</p>
        <p>6. 본 약관은 「금융소비자 보호법」 및 관련 법규에 따라 작성되었습니다.</p>
        <p>7. 추가 세부 사항은 은행의 공식 웹사이트 또는 지점에서 확인할 수 있습니다.</p>
      </div>
      <div class="agree-box">
        <label>
          <input
            type="checkbox"
            v-model="formData.agreeToTerms"
            required
          />
          약관에 동의합니다.
        </label>
      </div>
    </div>

    <!-- 옵션 선택 -->
    <div class="option-section block">
      <h2>옵션 선택</h2>
      <div class="options-grid">
        <div
          v-for="option in product.options"
          :key="option.id"
          class="option-card"
          :class="{ selected: formData.optionPk === option.id }"
          @click="selectOption(option.id)"
        >
          <p><strong>금리 유형:</strong> {{ option.intr_rate_type_nm }}</p>
          <p v-if="option.rsrv_type_nm"><strong>예약 타입:</strong> {{ option.rsrv_type_nm }}</p>
          <p><strong>저축 기간:</strong> {{ option.save_trm }}개월</p>
          <p><strong>금리:</strong> {{ option.intr_rate }}%</p>
        </div>
      </div>
    </div>

    <!-- 이름 입력 -->
    <div class="name-section block">
      <h2>가입자 정보</h2>
      <p>가입자 본인의 이름을 입력해주세요.</p>
      <input
        type="text"
        v-model="formData.name"
        placeholder="이름을 입력하세요"
      />
    </div>

    <!-- 가입 버튼 -->
    <div class="button-container">
      <button @click="handleSubmit" class="submit-button">가입하기</button>
    </div>

    <!-- 메시지 표시 -->
    <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>


<script setup>
import { reactive, ref } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from 'vue-router';

const userStore = useUserStore()
const store = useCounterStore()
const route = useRoute();
const router = useRouter();

let product = null;

const finPrdtCd = route.query.fin_prdt_cd; // 검색할 fin_prdt_cd
console.log(finPrdtCd)

if (store.depositoptions.find((item) => item.fin_prdt_cd === finPrdtCd)) {
  product = store.depositoptions.find((item) => item.fin_prdt_cd === finPrdtCd);
}

else {
  product = store.savingoptions.find((item) => item.fin_prdt_cd === finPrdtCd)
}


// 데이터 상태
const formData = reactive({
  name: "",
  optionPk: null, // 선택된 옵션 ID (단일 값)
  agreeToTerms: false,
});

const successMessage = ref("");
const errorMessage = ref("");

// 옵션 선택 처리
function selectOption(optionId) {
  formData.optionPk = optionId; // 단일 선택만 허용
}

// 가입 요청 처리
async function handleSubmit() {
  // 약관 동의 확인
  if (!formData.agreeToTerms) {
    errorMessage.value = "약관에 동의하지 않았습니다.";
    return;
  }

  // 옵션 선택 확인
  if (!formData.optionPk) {
    errorMessage.value = "옵션을 선택하지 않았습니다.";
    return;
  }

  // 본인 확인
  if (formData.name !== userStore.userInfo.realname) {
    console.log(userStore.userInfo)
    errorMessage.value = "본인 확인이 되지 않습니다.";
    return;
  }

  try {
    // 로컬 스토리지에서 토큰 가져오기
    const token = userStore.token;
    console.log(product)

    // 가입 요청 - Authorization 헤더 추가
    const response = await axios.post(
      "http://127.0.0.1:8000/finance/subscribed/", 
      {
        optionId: formData.optionPk,
        optionType: product.fin_prdt_nm.includes("적금") ? 0 : 1,
      },
      {
        headers: {
          'Authorization': `Token ${token}` // 또는 'Bearer ${token}'
        }
      }
    );

    successMessage.value = response.data.message;
    errorMessage.value = ""; 
    console.log("응답:", response.data);
    router.push({ name: 'ProfileView' });
  } catch (error) {
    console.error("서버 오류:", error.response ? error.response.data : error.message);
    successMessage.value = "";
    errorMessage.value = "상품 가입 중 오류가 발생했습니다.";
  }
}
</script>

<style scoped>
.registration-container {
  margin: 20px auto;
  padding: 20px;
  max-width: 800px;
  font-family: 'Noto Sans KR', sans-serif;
}

h1 {
  font-size: 28px;
  font-weight: bold;
  color: #326ecf;
  text-align: center;
  margin-bottom: 30px;
}

.block {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid #d2d2d2;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.terms-box {
  line-height: 1.6;
  color: #333;
  font-size: 14px;
  margin-bottom: 15px;
}

.agree-box {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.option-card {
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-card:hover {
  background-color: #eaf4fc;
  border-color: #326ecf;
}

.option-card.selected {
  background-color: #dbefff;
  border-color: #326ecf;
}

.name-section input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  margin-top: 10px;
}

.button-container {
  display: flex;
  justify-content: center; /* 버튼을 수평 중앙 정렬 */
  align-items: center; /* 버튼을 수직 중앙 정렬 */
  margin: 30px 0; /* 버튼 위아래 여백 */
}

.submit-button {
  width: 300px;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  color: white;
  background-color: #326ecf;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #2858a6;
}

.success-message {
  margin-top: 20px;
  font-size: 16px;
  color: green;
  text-align: center;
}

.error-message {
  margin-top: 10px;
  font-size: 14px;
  color: red;
  text-align: center;
}

</style>
