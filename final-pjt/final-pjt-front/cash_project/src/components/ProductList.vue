<template>
  <div class="product-card">
    <!-- 상품 제목과 은행명 -->
    <div class="product-header">
      <h3 class="product-title">{{ product.fin_prdt_nm }}</h3>
      <!-- 추천 상품 버튼 -->
      <button v-if="
          allDepositProducts.some(p => p.product_code === product.fin_prdt_cd) ||
          allSavingProducts.some(p => p.product_code === product.fin_prdt_cd) ||
          similarAgeDepositProducts.some(p => p.product_code === product.fin_prdt_cd) ||
          similarAgeSavingProducts.some(p => p.product_code === product.fin_prdt_cd)
        " class="recommend-button">
        추천 상품
      </button>
      <p class="product-bank">{{ product.kor_co_nm }}</p>
    </div>

    <!-- 금리 정보 -->
    <p class="product-rate">기본 연 {{ product.base_rate }}% ({{ product.base_trm || 'N/A' }}개월)</p>
    <p class="max-rate">최고 연 {{ product.max_rate }}%</p>

    <!-- 가입 정보와 버튼 -->
    <div class="product-actions">
      <div class="join-info">
        <p v-if="product.join_deny === 1" class="gray-badge">누구나 가입</p>
        <p v-if="product.join_way?.includes('인터넷') || product.join_way?.includes('스마트폰')" class="gray-badge">어디서나 가입</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: Object,
});

import { ref, onMounted } from 'vue';
import { useCounterStore } from "@/stores/counter.js";

const store = useCounterStore();

// 상품 배열 데이터
const allDepositProducts = ref([]);
const allSavingProducts = ref([]);
const similarAgeDepositProducts = ref([]);
const similarAgeSavingProducts = ref([]);

onMounted(async () => {
  try {
    allDepositProducts.value = store.allDepositProducts;
    allSavingProducts.value = store.allSavingProducts;
    similarAgeDepositProducts.value = store.similarAgeDepositProducts;
    similarAgeSavingProducts.value = store.similarAgeSavingProducts;
  } catch (error) {
    console.error("Error fetching products:", error);
  }
});
</script>

<style scoped>
/* 카드 전체 스타일 */
.product-card {
  border: 1px solid #326ECF;
  border-radius: 8px;
  padding: 15px;
  background-color: #f7faff; /* 매우 연한 푸른 빛 배경색 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  margin: 20px; /* 카드 간 넓은 마진 */
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* 헤더 스타일 */
.product-header {
  display: flex;
  align-items: center;
}

.product-title {
  font-size: 16px;
  font-weight: bold;
}

.product-bank {
  font-size: 14px;
  color: #555;
  margin-left: auto; /* 은행명은 오른쪽 끝으로 배치 */
}

/* 추천 상품 버튼 스타일 */
.recommend-button {
  background-color: #326ECF; /* 파란색 배경 */
  color: white;
  font-size: 14px;
  padding: 5px 10px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  margin-left: 10px; /* 상품명 오른쪽에 여백을 두고 배치 */
}

.recommend-button:hover {
  background-color: #0056b3; /* 버튼 호버 시 더 짙은 파란색 */
}

/* 금리 스타일 */
.product-rate {
  font-size: 14px;
  margin-bottom: 10px;
}

.max-rate {
  font-size: 14px;
  font-weight: bold;
  color: red;
  margin-bottom: 15px;
}

/* 가입 정보와 버튼 섹션 */
.product-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 가입 정보 뱃지 섹션 */
.join-info {
  display: flex;
  gap: 5px; /* 뱃지 간 간격 */
}

.gray-badge {
  background-color: #f1f1f1;
  color: #555;
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
