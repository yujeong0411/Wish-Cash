<template>
  <div class="profile-page">
    <nav class="profile-nav">
      <RouterLink :to="{ name: 'ProfileUpdateView' }">개인정보수정</RouterLink>
      <a href="#" @click.prevent="signout">회원탈퇴</a>
    </nav>

    <div class="banner-container">
      <!-- 왼쪽 섹션 -->
      <div class="banner-left">
        <div v-if="userProfile" class="profile-card">
          <h1 class="profile-greeting">
            <strong class="highlight">{{ userProfile.realname }}</strong> 고객님, 안녕하세요!
          </h1>
          <p class="profile-message">고객님을 위한 다양한 우대 혜택을 확인하세요.</p>
          <router-link :to="{ name: 'recommendedproduct' }" class="profile-link">맞춤형 금융상품 안내 ▶</router-link>
        </div>
        <div v-else class="loading-message">프로필 정보를 불러오는 중입니다...</div>
      </div>

      <!-- 오른쪽 섹션 -->
      <div class="banner-right">
        <div class="my-posts">
          <h3>내가 작성한 글</h3>
          <div class="posts-list" v-if="myArticles.length">
            <div
              v-for="article in displayedArticles"
              :key="article.id"
              class="post-item"
              @click="goToArticle(article.id)"
            >
              <span class="post-title">{{ article.title }}</span>
              <span class="post-date">{{ formatDate(article.created_at) }}</span>
            </div>
          </div>
          <div v-else class="no-posts">작성한 게시글이 없습니다.</div>
        </div>
      </div>
    </div>

    <!-- 메인 콘텐츠 -->
    <div class="main-content">
      <h2>나의 금융 정보</h2>
      <div class="filter-buttons">
        <button
          @click="setFilterType('deposit')"
          :class="{ active: filterType === 'deposit' }"
        >
          예금 보기
        </button>
        <button
          @click="setFilterType('saving')"
          :class="{ active: filterType === 'saving' }"
        >
          적금 보기
        </button>
      </div>

      <!-- 예금 가입 상품 -->
      <!-- 예금 상품 카드 리스트 -->
      <div v-if="filterType === 'deposit'">
        <h3>가입한 예금</h3>
        <div v-if="subscribedDeposits.length > 0" class="subscribed-items-container">
          <div
            v-for="(item, index) in subscribedDeposits"
            :key="index"
            class="subscribed-item"
            @click="handleCardClick(item)"
          >
          <div class="card" style="border: none; border-radius: 8px; position: relative;">
            <div class="card-body" style="background-color: #f3f8ff; padding: 20px;">
              <h4 class="card-title" style="color: #2d71c4; font-size: 1.5rem; font-weight: 600;">
                {{ item.product_name }}
              </h4>
              <p class="card-text" style="color: #333; font-size: 1rem; margin-bottom: 10px;">
                {{ item.bank_name }}
              </p>
              <p class="card-text" style="color: #333; font-size: 1rem; font-weight: 500;">
                금리 {{ item.intr_rate }}%
              </p>
              <!-- 해지 버튼 -->
              <button 
                class="unsubscribe-button"
                @click.stop="confirmUnsubscribe(item.id, 'deposit')"
                style="background-color: #2d71c4; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; font-size: 1rem; cursor: pointer; position: absolute; bottom: 15px; right: 15px; transition: background-color 0.3s;">
                해지
              </button>
            </div>
          </div>
          </div>
        </div>
      </div>

      <!-- 적금 상품 카드 리스트 -->
      <div v-if="filterType === 'saving'">
        <h3>가입한 적금</h3>
        <div v-if="subscribedSavings.length > 0" class="subscribed-items-container">
          <div
            v-for="(item, index) in subscribedSavings"
            :key="index"
            class="subscribed-item"
            @click="handleCardClick(item)"
          >
          <div class="card" style="border: none; border-radius: 8px; position: relative;">
            <div class="card-body" style="background-color: #f3f8ff; padding: 20px;">
              <h4 class="card-title" style="color: #2d71c4; font-size: 1.5rem; font-weight: 600;">
                {{ item.product_name }}
              </h4>
              <p class="card-text" style="color: #333; font-size: 1rem; margin-bottom: 10px;">
                {{ item.bank_name }}
              </p>
              <p class="card-text" style="color: #333; font-size: 1rem; font-weight: 500;">
                금리 {{ item.intr_rate }}%
              </p>
              <!-- 해지 버튼 -->
              <button 
                class="unsubscribe-button"
                @click.stop="confirmUnsubscribe(item.id, 'saving')"
                style="background-color: #2d71c4; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; font-size: 1rem; cursor: pointer; position: absolute; bottom: 15px; right: 15px; transition: background-color 0.3s;">
                해지
              </button>
            </div>
          </div>
          </div>
        </div>
      </div>
      <!-- 차트 섹션 -->
      <div class="chart-section" v-if="chartDataReady">
        <h3>{{ filterType === 'deposit' ? '예금 금리 차트' : '적금 금리 차트' }}</h3>
        <BarChart :chart-data="chartData" :chart-options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from "vue";
  import { storeToRefs } from "pinia";
  import { useUserStore } from "@/stores/user";
  import { useRouter, RouterView, RouterLink } from "vue-router";
  import { useArticleStore } from "@/stores/article.js";
  import { useCounterStore } from "@/stores/counter.js";
  import { format } from 'date-fns';
  import swal from "sweetalert2";
  import BarChart from "@/components/BarChart.vue";
  import axios from "axios";

  const router = useRouter();
  const store = useCounterStore();
  const userStore = useUserStore();
  const articleStore = useArticleStore();
  const { userProfile, isLogin } = storeToRefs(userStore)   // userprofile를 Pinia에서 가져옴
  const myArticles = ref([]);

  store.fetchProducts(userStore.userInfo.age)

  // 날짜 포맷팅 함수
  const formatDate = (date) => {
    return format(new Date(date), 'yyyy.MM.dd');
  };

  // 최근 3개의 게시글만 표시
  const displayedArticles = computed(() => {
    return myArticles.value.slice(0, 3);
  });

  // 게시글 상세 페이지로 이동
  const goToArticle = (articleId) => {
    router.push({ 
      name: 'ArticleDetailView', 
      params: { articleId: articleId } 
    });
  };

  const signout = function() {
    swal.fire({
      title: "회원탈퇴를 진행하시겠습니까?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#2858A6",
      cancelButtonColor: "#828282",
      confirmButtonText: "탈퇴 진행",
      cancelButtonText: "취소",
    }).then((result) => {
      if (result.isConfirmed) {  // selectedDelete 대신 result.isConfirmed 사용
        axios({
          method: "delete",
          url: `http://127.0.0.1:8000/accounts/profile/${userProfile.value.username}/delete/`,
          headers: {
            Authorization: `Token ${userStore.token}`,
          }
        }).then((res) => {
          swal.fire({
            title: "탈퇴 처리되었습니다.",
            icon: "success"
          }).then(() => {
            userStore.logoutUser(); // 확인 버튼 클릭 후 로그아웃
            router.push({ name: "MainView" });
          });
        }).catch((err) => {
          console.log(err);
        });
      } else {
        swal.fire({
          title: "탈퇴를 취소하셨습니다.",
          icon: "info"
        });
      }
    });
  }

  onMounted(async () => {
  if (isLogin.value) {
    // 프로필 조회
    userStore.getProfile();

    try {
      await articleStore.getArticleList();
      myArticles.value = articleStore.articleList
        .filter(article => article.user.username === userStore.userInfo.username)
        .reverse(); // 최신순 정렬
      await fetchSubscribedProducts("deposit");
      await fetchSubscribedProducts("saving");
    } catch (error) {
      console.error('게시글 조회 실패:', error);
    }
    }
  });

  const filterType = ref("deposit");

  // 추천 상품과 가입 상품 데이터
  const subscribedDeposits = ref([]);
  const subscribedSavings = ref([]);

  // 차트 데이터
  const rawChartData = ref({
    deposit: { labels: [], datasets: [{ data: [] }, { data: [] }] },
    saving: { labels: [], datasets: [{ data: [] }, { data: [] }] },
  });

  const chartDataReady = ref(false);

  const chartData = computed(() => {
    if (!chartDataReady.value) return { labels: [], datasets: [] };
    return {
      labels: rawChartData.value[filterType.value].labels,
      datasets: [
        {
          label: "기본 금리 (%)",
          data: rawChartData.value[filterType.value].datasets[0].data,
          backgroundColor: "rgba(75, 192, 192, 0.5)",
        },
        {
          label: "우대 금리 (%)",
          data: rawChartData.value[filterType.value].datasets[1].data,
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    };
  });

  const chartOptions = ref({
    responsive: true,
    plugins: {
      legend: { position: "top" },
    },
  });

  const fetchSubscribedProducts = async (type) => {
    try {
      const token = userStore.token;
      const res = await axios.get(`http://127.0.0.1:8000/finance/subscribed-list/`, {
        headers: { Authorization: `Token ${token}` },
        params: { type },
      });

      if (type === "deposit") subscribedDeposits.value = res.data.data;
      else if (type === "saving") subscribedSavings.value = res.data.data;

      rawChartData.value[type] = res.data.selected_chart || {
        labels: [],
        datasets: [{ data: [] }, { data: [] }],
      };

      if (type === filterType.value) {
        chartDataReady.value = true;
      }
    } catch (err) {
      console.error("차트 데이터를 가져오는 데 실패했습니다:", err.message);
    }
  };

  const confirmUnsubscribe = async (optionId, optionType) => {
    const userInput = prompt("본인의 이름을 입력해주세요:");
    if (userInput === userProfile.value.realname) {
      await unsubscribe(optionId, optionType);
    } else {
      alert("입력한 이름이 일치하지 않습니다.");
    }
  };

  const unsubscribe = async (optionId, optionType) => {
    try {
      const token = userStore.token;
      if (!token) {
        console.error("인증 토큰이 없습니다.");
        return;
      }

      // 해지 API 호출
      await axios.get(`http://127.0.0.1:8000/finance/unsubscribe/`, {
        headers: { Authorization: `Token ${token}` },
        params: { optionId, optionType },
      });

      // 성공 메시지 출력
      alert("해지되었습니다.");

      // 해지 후 가입 상품과 차트 데이터 새로 불러오기
      await fetchSubscribedProducts(optionType);
      chartDataReady.value = false; // 차트 데이터 로딩 상태 초기화
      rawChartData.value[optionType] = { labels: [], datasets: [{ data: [] }, { data: [] }] }; // 차트 초기화
      await fetchSubscribedProducts(optionType); // 차트 데이터 다시 가져오기
      chartDataReady.value = true; // 데이터 준비 완료 표시
    } catch (err) {
      console.error("구독 해지 실패:", err.response ? err.response.data : err.message);
    }
  };

  const setFilterType = (type) => {
    filterType.value = type;
    chartDataReady.value = false;
    fetchSubscribedProducts(type);
  };

  const handleCardClick = (item) => {
  router.push({ name: "productDetail", params: { fin_prdt_cd: item.fin_prdt_cd } });
};

const itemsPerPage = 3;
const currentPage = ref(1);

const paginatedDeposits = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return subscribedDeposits.value.slice(start, end);
});

const paginatedSavings = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return subscribedSavings.value.slice(start, end);
});

const totalPages = computed(() =>
  filterType.value === "deposit"
    ? Math.ceil(subscribedDeposits.value.length / itemsPerPage)
    : Math.ceil(subscribedSavings.value.length / itemsPerPage)
);

const hasMorePages = computed(() => totalPages.value > 1);

const changePage = (page) => {
  currentPage.value = Math.min(Math.max(1, page), totalPages.value);
};

  
</script>


<style scoped>
.profile-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-nav {
  text-align: right;
  margin-bottom: 20px;
  display: flex;  /* Flexbox 추가 */
  justify-content: flex-end;  /* 우측 정렬 유지 */
  gap: 20px;  /* 링크 사이 간격 */
}

.profile-nav a {
  color: #000000;
  font-size: 14px;
  text-decoration: none;
  
}

.profile-nav a:hover {
  text-decoration: underline;
  color: #0173ba;
}

.banner-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  gap: 20px;
}

.banner-left,
.banner-right {
  flex: 1;
  padding: 20px;
  border: 1px solid #d2d2d2;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.banner-left {
  background-image: url("@/assets/프로필배너.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.profile-card {
  color: #333;
}

.profile-greeting {
  font-size: 18px;
  margin-bottom: 10px;
}

.highlight {
  color: rgb(245, 161, 5);
}

.profile-message {
  margin: 10px 0;
  font-size: 14px;
  color: #3a3a3a;
}

.profile-link {
  color: #055181;
  font-weight: bold;
  text-decoration: none;
}

.profile-link:hover {
  text-decoration: underline;
}

.my-posts h3 {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #000407;
}

.post-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  border: 1px solid #d2d2d2;
  border-radius: 5px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.post-item:hover {
  background-color: #eaf4fc;
}

.post-title {
  font-size: 14px;
  color: #333;
}

.post-date {
  font-size: 12px;
  color: #666;
}

.no-posts {
  font-size: 14px;
  color: #666;
  text-align: center;
}

.main-content {
  margin-top: 20px;
}

.filter-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-buttons button {
  padding: 10px 20px;
  border: 1px solid #d2d2d2;
  background-color: white;
  cursor: pointer;
  border-radius: 5px;
}

.filter-buttons button.active {
  background-color: #0173ba;
  color: white;
}

.filter-buttons button:hover {
  background-color: #eaf4fc;
}

/* 상품 그리드 컨테이너 */
.subscribed-items-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* 카드가 1열에서 3열까지 변화 */
  gap: 20px;
  padding: 10px;
}

/* 개별 상품 카드 */
.subscribed-item {
  background-color: white;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.subscribed-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

/* 카드 헤더 (상품명, 은행명) */
.subscribed-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.subscribed-item-header strong {
  font-size: 16px;
  color: #0173ba;
}

.bank-name {
  font-size: 14px;
  color: #555;
}

/* 카드 본문 (금리 정보) */
.subscribed-item-body p {
  margin: 5px 0;
  font-size: 14px;
}

.interest-rate,
.bonus-rate {
  font-weight: bold;
}

.unsubscribe-button {
  position: absolute;
  bottom: 10px;
  right: 10px;
  padding: 6px 12px;
  background-color: #fff;
  color: #dc3545;
  border: 1px solid #dc3545;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.unsubscribe-button:hover {
  background-color: #dc3545;
  color: white;
}

/* 비어있을 때 메시지 */
.empty-message {
  text-align: center;
  color: #666;
  font-size: 14px;
  padding: 40px 0;
}

.chart-section {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #d2d2d2;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.chart-section h3 {
  margin-bottom: 20px;
  color: #0173ba;
  font-size: 18px;
  font-weight: bold;
}

.chart-section canvas {
  max-width: 100%;
  height: auto;
}

</style>