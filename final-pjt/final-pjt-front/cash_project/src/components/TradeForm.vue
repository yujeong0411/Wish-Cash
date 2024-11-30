<template>
  <div class="trade-form">
    <h2>💱 거래 폼</h2>
    <form @submit.prevent="submitTrade(selectedStock)">
      <p v-if="selectedStock">선택한 주식: <strong>{{ selectedStock.name }}</strong></p>

      <label>수량:</label>
      <input type="number" v-model.number="quantity" min="1" required />

      <label>거래 유형:</label>
      <select v-model="transactionType">
        <option value="BUY">매수</option>
        <option value="SELL">매도</option>
      </select>

      <button type="submit">거래 실행</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import { useUserStore } from "@/stores/user";

// Pinia 스토어 가져오기
const userStore = useUserStore();

// Props
defineProps({
  selectedStock: {
    type: Object,
    required: false,
  },
});

const emit = defineEmits(["tradeComplete"]);

// 데이터 변수
const quantity = ref(0);
const transactionType = ref("BUY"); // 기본값: BUY

// 메서드
const submitTrade = async (selectedStock) => {
  try {
    if (!selectedStock) {
      console.error("선택된 주식 정보가 없습니다.");
      return;
    }
    if (quantity.value <= 0) {
      console.error("거래 수량은 1 이상이어야 합니다.");
      return;
    }

    // 요청 데이터
    const requestData = {
      stock_symbol: selectedStock.symbol,
      quantity: quantity.value,
      transaction_type: transactionType.value,
    };

    console.log("보낼 데이터:", requestData);

    // API 요청
    const response = await axios.post("http://127.0.0.1:8000/game/trade/", requestData, {
      headers: {
        Authorization: `Token ${userStore.token}`, // 인증 토큰
      },
    });

    console.log("거래 성공:", response.data);

    // 부모 컴포넌트로 이벤트 전송
    emit("tradeComplete");
  } catch (error) {
    if (error.response) {
      console.error("거래 실패:", error.response.data);
    } else {
      console.error("거래 실행 중 오류 발생:", error);
    }
  }
};
</script>

<style scoped>
.trade-form {
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.trade-form h2 {
  font-size: 24px;
  color: #326ecf;
  margin-bottom: 10px;
}

.trade-form label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
}

.trade-form input,
.trade-form select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.trade-form button {
  background-color: #326ecf;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.trade-form button:hover {
  background-color: #224a8f;
}
</style>
