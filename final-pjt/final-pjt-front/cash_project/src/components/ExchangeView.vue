<template>
  <div class="card">
    <!-- 카드 헤더 -->
    <div class="card-header" @click="toggleCard">
      <h2 class="card-title">환율 계산기</h2>
      <span class="toggle-icon">{{ isCardOpen ? "▲" : "▼" }}</span>
    </div>

    <!-- 카드 내용 -->
    <div v-if="isCardOpen" class="card-content">
      <!-- 통화/금액 입력 -->
      <div class="card-section">
        <h3>통화 및 금액 입력</h3>
        <label for="currency">통화 선택:</label>
        <select v-model="selectedCurrency" class="input">
          <option value="" disabled>통화를 선택하세요</option>
          <option v-for="currency in exchange" :key="currency.cur_unit" :value="currency">
            {{ currency.cur_unit }} ({{ currency.cur_nm }})
          </option>
        </select>

        <label for="amount">금액 입력:</label>
        <input type="number" v-model.number="amount" id="amount" class="input" />
      </div>

      <!-- 환율 정보 -->
      <div v-if="selectedCurrency" class="card-section">
        <h3>환율 정보</h3>
        <p>매입환율 (TTB): {{ selectedCurrency.ttb }} KRW</p>
        <p>매도환율 (TTS): {{ selectedCurrency.tts }} KRW</p>
      </div>

      <!-- 환전 결과 -->
      <div v-if="selectedCurrency && amount > 0" class="card-section">
        <h3>환전 결과</h3>
        <p>원화 → 외화: <strong>{{ calculateForeign() }}</strong> {{ selectedCurrency.cur_unit }}</p>
        <p>외화 → 원화: <strong>{{ calculateKRW() }}</strong> KRW</p>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const exchange = computed(() => store.exchange); // Pinia store 데이터 가져오기
const selectedCurrency = ref(null); // 선택된 통화
const amount = ref(0); // 입력 금액
const isCardOpen = ref(false); // 카드 열림 상태

const calculateForeign = () => {
  if (!selectedCurrency.value || !amount.value) return 0;
  return (amount.value / selectedCurrency.value.tts).toFixed(2); // 원화 → 외화
};

const calculateKRW = () => {
  if (!selectedCurrency.value || !amount.value) return 0;
  return (amount.value * selectedCurrency.value.ttb).toFixed(2); // 외화 → 원화
};

const toggleCard = () => {
  isCardOpen.value = !isCardOpen.value;
};

onMounted(() => {
  store.saveExchange(); // Pinia store에서 환율 데이터 가져오기
});
</script>


<style scoped>
/* 카드 스타일 */
.card {
  border: 1px solid #d2d2d2;
  border-radius: 10px;
  overflow: hidden;
  width: 100%;
  max-width: 600px;
  margin: 20px auto;
  background-color: #ffffff;
}

.card-header {
  background-color: #2676a7;
  color: white;
  padding: 15px 20px;
  font-size: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.card-header:hover {
  background-color: #4a8cb5;
}

.card-title {
  margin: 0;
}

.toggle-icon {
  font-size: 16px;
}

.card-content {
  padding: 20px;
  background-color: #f9faff;
  animation: expand 0.3s ease-in-out;
}

.card-section {
  margin-bottom: 20px;
  padding: 10px 15px;
  background-color: #ffffff;
  border: 1px solid #d2d2d2;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-section h3 {
  font-size: 18px;
  color: #000000;
  margin-bottom: 10px;
}

.input {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  font-size: 14px;
  border: 1px solid #d2d2d2;
  border-radius: 8px;
  box-sizing: border-box;
}

.input:focus {
  border-color: #0173ba;
  outline: none;
}

.card-section p {
  margin: 5px 0;
  font-size: 16px;
  color: #333;
}

.card-section p strong {
  color: #0173ba;
}

/* 애니메이션 */
@keyframes expand {
  from {
    max-height: 0;
    opacity: 0;
  }
  to {
    max-height: 600px; /* 충분히 큰 값 */
    opacity: 1;
  }
}
</style>