<template>
  <div v-if="product" class="product-detail-container">
    <!-- 상품 정보 -->
    <div class="block product-info">
      <div class="info-header">
        <div>
          <h2>{{ product.fin_prdt_nm }}</h2>
          <p>{{ product.kor_co_nm }}</p>
        </div>
        <div class="rate-row">
          <div class="rate-item emphasis">
            <p>최고 금리</p>
            <h3>연 {{ product.max_rate }}%</h3>
          </div>
          <div class="rate-item">
            <p>기본 금리</p>
            <h3>
              연 {{ product.base_rate }}%
              <span class="term">({{ product.base_trm || 'N/A' }}개월)</span>
            </h3>
          </div>
        </div>
      </div>

      <div class="action-row">
        <div class="tag-buttons">
          <button v-if="product.join_deny === 1" class="tag">누구나 가입</button>
          <button
            v-if="product.join_way?.includes('인터넷') || product.join_way?.includes('스마트폰')"
            class="tag"
          >
            어디서나 가입
          </button>
        </div>
        <button v-if="
        product.join_deny === 1 &&
        (product.join_way?.includes('인터넷') || product.join_way?.includes('스마트폰')) &&
        !subscribedProduct.includes(product.fin_prdt_cd)
        "
        class="apply-button" @click="goToRegistration">가입하기</button>
      </div>
    </div>

    <!-- 상품 안내 -->
    <div class="block product-guide">
      <h2>상품 안내</h2>
      <table>
        <thead>
          <tr>
            <th>항목</th>
            <th>내용</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>가입방법</th>
            <td>{{ product.join_way }}</td>
          </tr>
          <tr>
            <th>대상</th>
            <td>{{ product.join_member }}</td>
          </tr>
          <tr>
            <th>우대조건</th>
            <td>{{ product.spcl_cnd }}</td>
          </tr>
          <tr>
            <th>기타</th>
            <td>{{ product.etc_note }}</td>
          </tr>
        </tbody>
      </table>

      <div class="additional-info">
        <h4>유의사항</h4>
        <p>▪ 이 설명서는 「금융소비자 보호에 관한 법률」 제19조 제1항에 따라 제공됩니다.</p>
        <p>▪ 금리변동형 정기예금은 금리 상승 시 유리할 수 있지만, 하락 시 불리할 수 있습니다.</p>
        <p>▪ 만기 해지 시 본인명의 계좌가 필요합니다.</p>

        <h4>예금자 보호</h4>
        <p>
          이 예금은 예금자보호법에 따라 원금과 소정의 이자를 합하여 1인당 "5천만원까지"
          ({{ product.kor_co_nm }}의 여타 보호 상품과 합산) 보호됩니다.
        </p>
      </div>
    </div>

    <!-- 금리 안내 -->
    <div class="block product-rates">
      <h2>금리 안내</h2>
      <table>
        <thead>
          <tr>
            <th>기간</th>
            <th>금리</th>
            <th>저축 금리 유형</th>
            <th v-if="product.options.some(option => option.rsrv_type_nm)">적립 유형</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="option in product.options" :key="option.intr_rate_type_nm">
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td v-if="option.rsrv_type_nm">{{ option.rsrv_type_nm }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script setup>
import { useRouter, useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import { ref, onMounted } from "vue";
import { useUserStore } from '@/stores/user';
import axios from 'axios';

const route = useRoute()
const router = useRouter();
const store = useCounterStore();
const userStore = useUserStore();

let product = null;

const finPrdtCd = route.params.fin_prdt_cd // 검색할 fin_prdt_cd

if (store.depositoptions.find((item) => item.fin_prdt_cd === finPrdtCd)) {
  product = store.depositoptions.find((item) => item.fin_prdt_cd === finPrdtCd);
}

else {
  product = store.savingoptions.find((item) => item.fin_prdt_cd === finPrdtCd)
}

const goToRegistration = () => {
  router.push({ 
    name: 'bankregistrationform', 
    query: { fin_prdt_cd: finPrdtCd } // 원하는 쿼리 파라미터 추가
  });
};

const subscribedProduct = ref([])

const fetchSubscribedProducts = async (type) => {
    try {
      const token = userStore.token;
      const res = await axios.get(`http://127.0.0.1:8000/finance/subscribed-list/`, {
        headers: { Authorization: `Token ${token}` },
        params: { type },
      });

      const subProduct = res.data.data;

      for (const sub of subProduct) {
        subscribedProduct.value.push(sub.fin_prdt_cd)
      }
    } catch (err) {
      console.error(err);
    }
  };

onMounted(async () => {
  try {
    await fetchSubscribedProducts("deposit");
    await fetchSubscribedProducts("saving");
  } catch (error) {
    console.error(error);
  }
});

</script>


<style scoped>
.product-detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: #f9f9f9; /* 페이지 배경 */
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.block {
  border: 1px solid #d2d2d2;
  border-radius: 8px;
  padding: 20px;
  background-color: white;
}

h2 {
  color: #000000;
  font-size: 24px;
  font-weight: 700;
}

.rate-row {
  display: flex;
  gap: 20px;
  align-items: center;
}

.rate-item {
  text-align: center;
}

.rate-item h3 {
  font-size: 20px;
  margin: 5px 0;
  font-weight: bold;
}

.rate-item.emphasis h3 {
  color: #0173BA;
}

.action-row {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.tag-buttons {
  display: flex;
  gap: 10px;
}

.tag {
  padding: 8px 12px;
  font-size: 14px;
  color: #666;
  background-color: #f1f1f1;
  border: 1px solid #d2d2d2;
  border-radius: 5px;
  cursor: default;
}

.apply-button {
  background-color: #0173BA;
  color: white;
  border: none;
  padding: 10px 15px;
  font-size: 14px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.apply-button:hover {
  background-color: #306d92;
}

.product-guide table,
.product-rates table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.product-guide th,
.product-guide td,
.product-rates th,
.product-rates td {
  border: 1px solid #d2d2d2;
  padding: 10px;
  text-align: left;
}

.product-guide th,
.product-rates th {
  background-color: #f4f4f4;
  color: rgb(0, 0, 0);
  font-weight: 500;
}

.product-guide td,
.product-rates td {
  background-color: #f9f9f9;
}

.additional-info h4 {
  margin-top: 20px;
  font-size: 18px;
  color: #000000;
}

</style>
