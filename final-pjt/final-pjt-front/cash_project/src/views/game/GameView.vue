<template>
  <div id="game-view">
    <header class="game-header">
      <h1>📈 모의 주식 게임</h1>
      <p>실제 주식 거래처럼 연습하고 경험을 쌓아보세요!</p>
    </header>

    <main class="game-content">
      <div class="left-panel">
        <Portfolio ref="portfolioRef" />
        <StockList @selectStock="selectStock" />
      </div>
      <div class="right-panel">
        <TransactionHistory ref="transactionHistoryRef" />
      </div>
    </main>

    <!-- 거래폼 모달 -->
    <div v-if="isTradeModalVisible" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>주식 거래</h2>
        <TradeForm :selectedStock="selectedStock" @tradeComplete="handleTradeComplete" />
        <button class="close-btn" @click="closeModal">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Portfolio from "@/components/Portfolio.vue";
import StockList from "@/components/StockList.vue";
import TradeForm from "@/components/TradeForm.vue";
import TransactionHistory from "@/components/TransactionHistory.vue";
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore()

// 선택된 주식을 관리하는 상태
const selectedStock = ref(null);

// Portfolio 컴포넌트와 TransactionHistory 컴포넌트의 메서드를 호출하기 위한 참조
const portfolioRef = ref(null);
const transactionHistoryRef = ref(null);

// 거래폼 모달의 가시성 상태
const isTradeModalVisible = ref(false);

// StockList에서 선택된 주식을 설정
const selectStock = (stock) => {
  selectedStock.value = stock;
  isTradeModalVisible.value = true;  // 모달 열기
  console.log(selectedStock.value)
};

// 거래 후 포트폴리오 및 거래 내역 업데이트
const updatePortfolio = () => {
  if (portfolioRef.value && typeof portfolioRef.value.fetchPortfolio === "function") {
    portfolioRef.value.fetchPortfolio(); // 포트폴리오 갱신
  } else {
    console.error("fetchPortfolio 메서드를 찾을 수 없습니다.");
  }

  if (transactionHistoryRef.value && typeof transactionHistoryRef.value.fetchTransactions === "function") {
    transactionHistoryRef.value.fetchTransactions(); // 거래 내역 갱신
  } else {
    console.error("fetchTransactions 메서드를 찾을 수 없습니다.");
  }
};

// 거래 완료 후 모달 닫기
const handleTradeComplete = () => {
  updatePortfolio();  // 거래 후 포트폴리오 갱신
  closeModal();       // 거래 완료 후 모달 닫기
};

// 모달을 닫는 함수
const closeModal = () => {
  isTradeModalVisible.value = false; // 모달 닫기
};

store.fetchAndSaveStockData();
</script>

<style scoped>
#game-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

/* 헤더 스타일 */
.game-header {
  text-align: center;
  margin-bottom: 20px;
}

.game-header h1 {
  font-size: 36px;
  color: #326ecf;
}

.game-header p {
  font-size: 16px;
  color: #555;
}

/* 레이아웃 스타일 */
.game-content {
  display: flex;
  gap: 20px;
}

.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
}

.close-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #326ecf;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #2858b2;
}
</style>
