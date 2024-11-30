<template>
  <div class="portfolio">
    <h2>📊 나의 포트폴리오</h2>
    <p>💰 잔액: <span>{{ balance.toFixed(2) }}</span> 원</p>
    <table>
      <thead>
        <tr>
          <th>종목 이름</th>
          <th>보유 수량</th>
          <th>구매 가격</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in displayedPortfolio" :key="stock.stock_symbol">
          <td>{{ stock.stock_name }}</td>
          <td>{{ stock.quantity }}</td>
          <td>{{ stock.purchase_price }}</td>
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
import { useUserStore } from "@/stores/user";

// Pinia 스토어 가져오기
const userStore = useUserStore();

// 상태 관리 변수
const balance = ref(0);
const portfolio = ref([]);
const currentPage = ref(1);  // 현재 페이지
const itemsPerPage = ref(6);  // 한 페이지에 표시할 포트폴리오 개수

// 포트폴리오 데이터 가져오기
const fetchPortfolio = async () => {
  try {
    const token = userStore.token; // 인증 토큰 가져오기
    console.log('#', token)
    if (!token) {
      console.warn("로그인이 필요합니다.");
      return;
    }

    const response = await axios.get("http://127.0.0.1:8000/game/portfolio/", {
      headers: { Authorization: `Token ${token}` },
    });
    balance.value = response.data.balance; // 잔액 설정
    portfolio.value = response.data.portfolio; // 포트폴리오 설정
  } catch (error) {
    console.error("포트폴리오를 가져오는 중 오류 발생:", error);
  }
};

// 한 페이지에 표시할 포트폴리오 목록을 반환하는 computed 속성
const displayedPortfolio = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return portfolio.value.slice(start, end); // 페이지에 맞는 포트폴리오만 반환
});

// 총 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(portfolio.value.length / itemsPerPage.value); // 전체 포트폴리오를 itemsPerPage로 나눈 값의 올림
});

// 페이지 변경 함수
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return; // 유효한 페이지 번호만 처리
  currentPage.value = page;
};

defineExpose({
  fetchPortfolio,
});

// 컴포넌트가 마운트될 때 포트폴리오 데이터 로드
onMounted(fetchPortfolio);
</script>

<style scoped>
.portfolio {
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.portfolio h2 {
  font-size: 24px;
  color: #326ecf;
  margin-bottom: 10px;
}

.portfolio table {
  width: 100%;
  border-collapse: collapse;
}

.portfolio th,
.portfolio td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
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
