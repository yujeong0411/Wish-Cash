<template>
  <div class="article-container">
    <!-- 타이틀 -->
    <header class="header">
      <h1>적금 조회</h1>
    </header>

    <!-- 필터 섹션 -->
    <section class="form-description">
      <div class="filter-content">
        <div class="filter-group">
          <select v-model="selectedBank" class="filter-select">
            <option value="">은행 선택</option>
            <option v-for="bank in uniqueBanks" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>

          <select v-model="baseRateSort" class="filter-select">
            <option value="">기준 금리순</option>
            <option value="asc">기준 금리 낮은 순</option>
            <option value="desc">기준 금리 높은 순</option>
          </select>

          <select v-model="maxRateSort" class="filter-select">
            <option value="">최고 금리순</option>
            <option value="asc">최고 금리 낮은 순</option>
            <option value="desc">최고 금리 높은 순</option>
          </select>
        </div>

        <div class="checkbox-group">
          <label class="filter-checkbox">
            <input type="checkbox" v-model="filterByJoinWay" />
            어디서나 가입
          </label>

          <label class="filter-checkbox">
            <input type="checkbox" v-model="filterByJoinDeny" />
            누구나 가입
          </label>
        </div>
      </div>
    </section>

    <hr class="divider" />

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading">데이터를 로드 중입니다...</div>

    <!-- 상품 리스트 -->
    <div v-else class="products-container">
      <ProductList
        v-for="product in sortedProducts"
        :key="product.fin_prdt_cd"
        :product="product"
        @click="goToDetail(product.fin_prdt_cd)"
      />
      <div v-if="sortedProducts.length === 0" class="no-results">
        선택된 조건에 맞는 상품이 없습니다.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useCounterStore } from '@/stores/counter';
import ProductList from '@/components/ProductList.vue';
import { useRouter } from 'vue-router';

const store = useCounterStore();
const products = ref([]); // 모든 상품 데이터
const selectedBank = ref(''); // 선택된 은행
const baseRateSort = ref(''); // 기준 금리 정렬 옵션
const maxRateSort = ref(''); // 최고 금리 정렬 옵션
const filterByJoinDeny = ref(false); // join_deny 필터링 여부
const filterByJoinWay = ref(false); // join_way 필터링 여부
const loading = ref(true); // 로딩 상태
const router = useRouter();

// 초기 데이터 로드
onMounted(async () => {
  if (store.savingoptions.length === 0) {
    await store.getSavingProducts(); // 데이터를 로드
  }
  products.value = store.savingoptions;
  loading.value = false; // 로딩 완료
});

// 은행 리스트 추출
const uniqueBanks = computed(() => {
  const banks = products.value.map((product) => product.kor_co_nm || 'Unknown Bank');
  return [...new Set(banks)]; // 중복 제거
});

// 필터링된 상품 리스트
const filteredProducts = computed(() => {
  let filtered = [...products.value];

  // 은행 필터링
  if (selectedBank.value) {
    filtered = filtered.filter((product) => product.kor_co_nm === selectedBank.value);
  }

  // join_deny 필터링
  if (filterByJoinDeny.value) {
    filtered = filtered.filter((product) => product.join_deny === 1);
  }

  // join_way 필터링
  if (filterByJoinWay.value) {
    filtered = filtered.filter(
      (product) =>
        product.join_way?.includes('인터넷') || product.join_way?.includes('스마트폰')
    );
  }

  return filtered;
});

// 정렬된 상품 리스트
const sortedProducts = computed(() => {
  let sorted = [...filteredProducts.value];

  // 기준 금리 정렬
  if (baseRateSort.value === 'asc') {
    sorted.sort((a, b) => (a.base_rate || 0) - (b.base_rate || 0));
  } else if (baseRateSort.value === 'desc') {
    sorted.sort((a, b) => (b.base_rate || 0) - (a.base_rate || 0));
  }

  // 최고 금리 정렬
  if (maxRateSort.value === 'asc') {
    sorted.sort((a, b) => (a.max_rate || 0) - (b.max_rate || 0));
  } else if (maxRateSort.value === 'desc') {
    sorted.sort((a, b) => (b.max_rate || 0) - (a.max_rate || 0));
  }

  return sorted;
});

// 정렬 상태 초기화 로직
watch(baseRateSort, (newValue) => {
  if (newValue) {
    maxRateSort.value = ''; // 기준 금리 정렬 변경 시 최고 금리 정렬 초기화
  }
});

watch(maxRateSort, (newValue) => {
  if (newValue) {
    baseRateSort.value = ''; // 최고 금리 정렬 변경 시 기준 금리 정렬 초기화
  }
});

// 상세 페이지 이동
const goToDetail = (fin_prdt_cd) => {
  router.push({ name: 'productDetail', params: { fin_prdt_cd } });
};
</script>

<style scoped>
/* 공통 스타일 */
.article-container {
  width: 100%;
  min-width: 800px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #ffffff;
  font-family: "Noto Sans KR", sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  position: relative;
}

.header::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(to right, #91919f, #8caff5);
}

h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111111;
  margin: 0;
  letter-spacing: -0.5px;
}

/* 필터 섹션 */
.form-description {
  background: linear-gradient(145deg, #f8f9fd 0%, #f2f4f8 100%);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
}

.filter-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-group {
  display: flex;
  gap: 20px;
}

.filter-select {
  flex: 1;
  padding: 10px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  font-size: 14px;
}

.checkbox-group {
  display: flex;
  gap: 20px;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.divider {
  border: 0;
  height: 1px;
  background: #d2d2d2;
  margin: 30px 0;
}

/* 상품 리스트 */
.products-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.no-results {
  grid-column: span 2;
  text-align: center;
  padding: 40px;
  color: #666;
  background-color: #f8f9fd;
  border-radius: 8px;
}

@media (max-width: 1024px) {
  .products-container {
    grid-template-columns: 1fr;
  }
}
</style>
