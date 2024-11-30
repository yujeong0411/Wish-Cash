<template>
  <div class="transaction-history">
    <h2>거래 내역</h2>
    
    <!-- 거래 내역 테이블 -->
    <table v-if="currentTransactions.length > 0">
      <thead>
        <tr>
          <th>종목 이름</th>
          <th>거래 유형</th>
          <th>수량</th>
          <th>가격</th>
          <th>날짜</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(transaction, index) in currentTransactions" :key="index">
          <td>{{ transaction.stock }}</td>
          <td>{{ transaction.transaction_type }}</td>
          <td>{{ transaction.quantity }}</td>
          <td>{{ transaction.price }} 원</td>
          <td>{{ formatTimestamp(transaction.timestamp) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>거래 내역이 없습니다.</p>

    <!-- 페이징 -->
    <div class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="previousPage">이전</button>
      <span>{{ currentPage }} / {{ totalPages }} 페이지</span>
      <button 
        :disabled="currentPage === totalPages" 
        @click="nextPage">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from "@/stores/user";

// Pinia 스토어 가져오기
const userStore = useUserStore();

// 상태 관리
const transactions = ref([]);
const currentPage = ref(1);
const transactionsPerPage = ref(15);  // 한 페이지에 표시할 거래 내역 수

// 거래 내역을 가져오는 함수
const fetchTransactions = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/game/transactions/', {
      headers: {
        'Authorization': `Token ${userStore.token}`
      }
    });
    transactions.value = response.data;
  } catch (error) {
    console.error('Error fetching transactions:', error);
  }
};

// 거래 내역 날짜 형식 변환 함수
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
};

// 현재 페이지에 해당하는 거래 내역
const currentTransactions = computed(() => {
  const startIndex = (currentPage.value - 1) * transactionsPerPage.value;
  const endIndex = startIndex + transactionsPerPage.value;
  return transactions.value.slice(startIndex, endIndex);
});

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(transactions.value.length / transactionsPerPage.value);
});

// 이전 페이지로 이동
const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// 다음 페이지로 이동
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

// 컴포넌트가 마운트될 때 거래 내역을 가져옴
onMounted(fetchTransactions);

// 노출할 메서드
defineExpose({
  fetchTransactions,
});
</script>

<style scoped>
.transaction-history {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fbfbfb;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

th {
  background-color: #326ECF;
  color: white;
}

td {
  background-color: #f7faff;
}

h2 {
  text-align: center;
  color: #326ECF;
}

/* 페이징 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #326ecf;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.pagination span {
  align-self: center;
  font-size: 16px;
}
</style>
