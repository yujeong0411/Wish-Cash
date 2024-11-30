<template>
  <div class="product-container">
    <div class="section-header">
      <h2>고객님들이 선택한 <strong class="highlight">BEST</strong> 인기상품</h2>
      <p>가장 많이 사랑받은 인기상품입니다.</p>
    </div>

    <!-- 언더라인 탭 메뉴로 변경 -->
    <ul class="nav-underline">
      <li class="nav-item">
        <a 
          href="#"
          class="nav-link"
          :class="{ active: activeTab === 'deposit' }"
          @click.prevent="activeTab = 'deposit'"
        >
          예금상품
        </a>
      </li>
      <li class="nav-item">
        <a 
          href="#"
          class="nav-link"
          :class="{ active: activeTab === 'saving' }"
          @click.prevent="activeTab = 'saving'"
        >
          적금상품
        </a>
      </li>
    </ul>
    
    <div class="section-content">
      <div v-if="activeTab === 'deposit'">
        <!-- 전체 고객 - 예금 -->
        <div class="product-section">
          <h3 class="section-title">전체 고객</h3>
          <div class="card-list">
            <div
            v-for="(product, index) in allDepositProducts"
            :key="index"
            class="card"
            @click="goToDetail(product.product_code)"
            >
            <div class="badge">예금 BEST</div>
              <h4>{{ product.product_name }}</h4>
              <p class="bank-name">{{ product.bank_name }}</p>
              <div class="rate-container">
                <span>최고</span>
                <strong>연 {{ product.highest_intr_rate2 }}%</strong>
              </div>
            </div>
          </div>
        </div>

        <!-- 비슷한 나이대 고객 - 예금 -->
        <div class="product-section">
          <h3 class="section-title">비슷한 나이대 고객</h3>
          <div class="card-list">
            <div
              v-for="(product, index) in similarAgeDepositProducts"
              :key="index"
              class="card"
              @click="goToDetail(product.product_code)"
            >
              <div class="badge">예금 BEST</div>
              <h4>{{ product.product_name }}</h4>
              <p class="bank-name">{{ product.bank_name }}</p>
              <div class="rate-container">
                <span>최고</span>
                <strong>연 {{ product.highest_intr_rate2 }}%</strong>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'saving'">
        <!-- 전체 고객 - 적금 -->
        <div class="product-section">
          <h3 class="section-title">전체 고객</h3>
          <div class="card-list">
            <div
              v-for="(product, index) in allSavingProducts"
              :key="index"
              class="card"
              @click="goToDetail(product.product_code)"
            >
              <div class="badge">적금 BEST</div>
              <h4>{{ product.product_name }}</h4>
              <p class="bank-name">{{ product.bank_name }}</p>
              <div class="rate-container">
                <span>최고</span>
                <strong>연 {{ product.highest_intr_rate2 }}%</strong>
              </div>
            </div>
          </div>
        </div>

        <!-- 비슷한 나이대 고객 - 적금 -->
        <div class="product-section">
          <h3 class="section-title">비슷한 나이대 고객</h3>
          <div class="card-list">
            <div
              v-for="(product, index) in similarAgeSavingProducts"
              :key="index"
              class="card"
              @click="goToDetail(product.product_code)"
            >
              <div class="badge">적금 BEST</div>
              <h4>{{ product.product_name }}</h4>
              <p class="bank-name">{{ product.bank_name }}</p>
              <div class="rate-container">
                <span>최고</span>
                <strong>연 {{ product.highest_intr_rate2 }}%</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useCounterStore } from "@/stores/counter.js";

const activeTab = ref("deposit");
const store = useCounterStore()

const allDepositProducts = ref([]);
const allSavingProducts = ref([]);
const similarAgeDepositProducts = ref([]);
const similarAgeSavingProducts = ref([]);

const router = useRouter();

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

// 상세 페이지로 이동
const goToDetail = (fin_prdt_cd) => {
  router.push({
    name: "productDetail",
    params: { fin_prdt_cd },
    query: { source: "cardClick" },
  });
};
</script>

<style scoped>
.product-container {
  background-color: #ffffff;
  padding: 40px;
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}


.section-header h2 {
  font-size: 32px;
  font-weight: bold;
  color: #000000;
  margin: 0;
  padding-bottom: 6px;
}

.section-header p {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
}

.subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
}

/* 언더라인 메뉴 스타일 */
.nav-underline {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0 0 30px 0;
  justify-content: center;
}

.nav-item {
  margin-right: 20px;
}

.nav-link {
  text-decoration: none;
  font-size: 16px;
  color: #747577;
  padding: 8px 0;
  transition: color 0.3s ease, border-bottom 0.3s ease;
  display: inline-block;
  margin-bottom: -1px;
}

.nav-link.active {
  color: #2858A6;
  font-weight: bold;
  border-bottom: 2px solid #2858A6;
}

.nav-link:hover {
  color: #2858A6;
}

.section-title {
  text-align: left;
  font-size: 20px;
  margin: 30px 0 20px;
  color: #333;
  font-weight: bold;
}

.card-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: left;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  border: 1px solid #eee;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(40, 88, 166, 0.15);
  border-color: #2858A6;
}

.badge {
  background-color: #2858A6;
  color: #fff;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  display: inline-block;
  margin-bottom: 15px;
  font-weight: 500;
}

h4 {
  font-size: 20px;
  font-weight: bold;
  margin: 15px 0;
  color: #333;
  line-height: 1.4;
}

.bank-name {
  font-size: 15px;
  color: #666;
  margin: 10px 0;
}

.rate-container {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.rate-container span {
  font-size: 14px;
  color: #666;
  display: block;
  margin-bottom: 5px;
}

.rate-container strong {
  font-size: 24px;
  font-weight: bold;
  color: #2858A6;
}

.highlight {
  color: orange;
}

@media (max-width: 768px) {
  .product-container {
    padding: 20px;
  }

  .section-header h2 {
    font-size: 24px;
  }

  .card-list {
    grid-template-columns: 1fr;
  }
}
</style>