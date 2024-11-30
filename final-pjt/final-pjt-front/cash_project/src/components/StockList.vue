<template>
  <div class="stock-list">
    <h2>📋 주식 목록</h2>
    <table>
      <thead>
        <tr>
          <th>종목 코드</th>
          <th>종목 이름</th>
          <th>현재 가격</th>
          <th>거래</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in displayedStocks" :key="stock.symbol">
          <td>{{ stock.symbol }}</td>
          <td>{{ stock.name }}</td>
          <td>
            {{ stock.current_price }} 원
            <span :style="getPriceChangeStyle(stock.percent_change)">
              <!-- 화살표 추가 -->
              <span v-if="stock.percent_change > 0">↑</span>
              <span v-else-if="stock.percent_change < 0">↓</span>
              <span v-else>-</span>
              ({{ stock.percent_change }}%)
            </span>
          </td>
          <td>
            <button @click="selectStock(stock)">거래</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 페이징 컨트롤 -->
    <div class="pagination">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">이전</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

// 상태 관리 변수
const stocks = ref([]);
const currentPage = ref(1);  // 현재 페이지
const itemsPerPage = ref(10);  // 한 페이지에 표시할 주식 개수

// Emit 정의
const emit = defineEmits(["selectStock"]);

// 주식 데이터 가져오기 함수
const fetchStocks = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/game/stocks/");
    stocks.value = response.data; // API에서 받은 데이터를 stocks 변수에 저장
  } catch (error) {
    console.error("주식 데이터를 가져오는 중 오류 발생:", error);
  }
};

// 주식 선택 이벤트
const selectStock = (stock) => {
  emit("selectStock", stock); // 부모 컴포넌트로 선택한 주식 전달
};

// 한 페이지에 표시할 주식 목록을 반환하는 computed 속성
const displayedStocks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return stocks.value.slice(start, end); // 페이지에 맞는 주식만 반환
});

// 총 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(stocks.value.length / itemsPerPage.value); // 전체 항목을 itemsPerPage로 나눈 값의 올림
});

// 페이지 변경 함수
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return; // 유효한 페이지 번호만 처리
  currentPage.value = page;
};

const getPriceChangeStyle = (percentChange) => {
  if (percentChange > 0) {
    return { color: 'red' }; // 가격 상승: 빨간색
  } else if (percentChange < 0) {
    return { color: 'blue' }; // 가격 하락: 파란색
  } else {
    return { color: 'black' }; // 변동 없음: 검정색
  }
};

// 컴포넌트가 마운트될 때 주식 데이터 로드
onMounted(fetchStocks);
</script>

<style scoped>
.stock-list {
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stock-list h2 {
  font-size: 24px;
  color: #326ecf;
  margin-bottom: 10px;
}

.stock-list table {
  width: 100%;
  border-collapse: collapse;
}

.stock-list th,
.stock-list td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.stock-list button {
  background: #326ecf;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.stock-list button:hover {
  background: #244f9c;
}

/* 페이징 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 5px 15px;
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
  margin: 0 10px;
  align-self: center;
}
</style>
