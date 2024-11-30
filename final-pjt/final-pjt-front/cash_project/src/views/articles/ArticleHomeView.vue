<template>
  <div class="article-container">
    <!-- 타이틀 -->
    <header class="header">
      <h1>자주하는 질문</h1>
    </header>

    <section class="form-description">
      <div class="description-content">
        <div class="link-container">
          <div class="links">
            <!-- 왼쪽 열 -->
            <div class="info-section">
              <p class="info-title">고객센터 전화 안내</p>
              <p class="info-content">
                - 1599-1234 / 1577-1234 / 1544-1234<br>
                - 해외에서 전화 시 82-2-5678-1234<br>
                - LMS 발신번호 1644-1345
              </p>
            </div>
            
            <!-- 오른쪽 열 -->
            <div class="info-section">
              <p class="info-title">수어 상담</p>
              <p class="info-content">
                - 카카오톡 : wishcashface1 / 2<br>
                - 씨토크 : 070-7979-9000 / 9001
              </p>
            </div>

            <!-- 왼쪽 열 -->
            <div class="info-section">
              <p class="info-title">상담 시간</p>
              <p class="info-content">
                평일 09:00 ~ 18:00<br>
                챗봇 상담 가능
              </p>
            </div>

            <!-- 오른쪽 열 -->
            <div class="info-section">
              <p class="info-title">바로가기</p>
              <div class="info-content">
                <RouterLink class="description-link" :to="{ name: 'ProfileUpdateView' }">
                  고객 정보 수정 (클릭)
                </RouterLink>
                <RouterLink class="description-link" :to="{ name: 'MapView' }">
                  은행/ATM 찾기 (클릭)
                </RouterLink>
              </div>
            </div>
          </div>
          <img src="@/assets/게시글아이콘.png" alt="게시글 아이콘" class="description-img">
        </div>
      </div>
    </section>

    <hr class="divider">

     <!-- 질문 검색 -->
     <section class="search-section">
      <div class="search-header">
        <div>
          <h3 class="highlight">자주찾는 질문 검색하기</h3>
          <p>Wish Cash뿐만 아니라 다른 회원들의 의견도 들을 수 있어요.</p>
        </div>
        <RouterLink class="create-link" :to="{ name: 'ArticleCreateView' }">질문하기</RouterLink>
      </div>
      <!-- 검색 입력창 -->
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="검색어를 입력하세요"
          class="search-input"
          @input="handleSearch"
        >
      </div>
    </section>
    
  
    <!-- 게시글 리스트 -->
    <div class="article-list">
      <!-- 리스트 헤더 -->
      <div class="list-header">
        <span>제목</span>
        <span>닉네임</span>
        <span>날짜</span>
      </div>

      <!-- 게시글 목록 -->
      <div
        v-for="(article, index) in paginatedArticle"
        :key="index"
        class="list-item"
        @click="articleDetail(article.id)"
      >
        <span class="list-title">{{ article.title }}</span>
        <span class="list-nickname">{{ article.user.nickname }}</span>
        <span class="list-date">{{ formatDate(article.created_at) }}</span>
      </div>
    </div>

    <!-- 검색 결과가 없을 때 메시지 -->
    <div v-if="paginatedArticle.length === 0" class="no-results">
      검색 결과가 없습니다.
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button @click="updatePagination(currentPage - 1)" :disabled="currentPage === 1">
        이전
      </button>
      <span>{{ currentPage }} of {{ totalPage }} 페이지</span>
      <button @click="updatePagination(currentPage + 1)" :disabled="currentPage === totalPage">
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useArticleStore } from "@/stores/article";
import { RouterLink, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { format } from "date-fns";

const userStore = useUserStore();
const router = useRouter();
const articleStore = useArticleStore();
const articlePage = 5;
const newArticle = ref([]);
const currentPage = ref(1);
const searchQuery = ref(''); // 검색어 상태 추가

// 날짜 변환
const formatDate = function (date) {
  return format(new Date(date), "yyyy-MM-dd");
};

// 전체 게시글 조회
onMounted(() => {
  articleStore.getArticleList();
});


watch(
  () => articleStore.articleList,
  (newArticleList) => {
    newArticle.value = newArticleList;
  }
);

// 검색 기능 구현
const handleSearch = () => {
  currentPage.value = 1; // 검색 시 첫 페이지로 
};

// 검색된 게시글 필터링
const filteredArticles = computed(() => {
  if (!searchQuery.value) {
    return newArticle.value;
  }
  return newArticle.value.filter(article => 
    article.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// 최근 게시글로 정렬 (검색 결과에 대해)
const reversedArticles = computed(() => {
  return [...filteredArticles.value].reverse();
});

// 페이지 계산
const totalPage = computed(() => {
  return Math.ceil(reversedArticles.value.length / articlePage);
});

// 페이지 변경 계산
const paginatedArticle = computed(() => {
  const start = (currentPage.value - 1) * articlePage;
  const end = start + articlePage;
  return reversedArticles.value.slice(start, end);
});

const updatePagination = function (page) {
  currentPage.value = page;
};

// 게시글 디테일
const articleDetail = function (articleId) {
  router.push({ name: "ArticleDetailView", params: { articleId: articleId } });
};
</script>



<style scoped>
/* 기본 스타일 */
.article-container {
  width: 100%;
  min-width: 800px;  /* 최소 너비 설정 */
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #ffffff;
  box-sizing: border-box;
  font-family: 'Noto Sans KR', sans-serif;
  white-space: nowrap;  /* 줄바꿈 방지 */
  /* overflow-x: auto;    가로 스크롤 활성화 */
}

/* 타이틀 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  position: relative;
}

.header::after {
  content: '';
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

/* 설명 박스 */
.form-description {
  background: linear-gradient(145deg, #f8f9fd 0%, #f2f4f8 100%);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
}

.link-container {
  display: flex;
  justify-content: space-between;
  gap: 30px;
  min-width: 700px;
  overflow-x: visible;
  white-space: nowrap;  /* 줄바꿈 허용 */
}


.description-img {
  width: 200px;  /* 아이콘 크기 조절 */
  height: auto;
  object-fit: contain;
  align-self: flex-start;  /* 상단 정렬 */
  flex-shrink: 0;  /* 이미지 크기 유지 */
}

/* 설명 박스 내부 스타일 추가 */
.links {
  display: grid;  /* flex에서 grid로 변경 */
  grid-template-columns: 1fr 1fr;
  gap: 20px 40px;
  width: 100%;
  min-width: 500px;  /* 최소 너비 설정 */
  white-space: nowrap;  /* 줄바꿈 허용 */
  flex: 1;  /* 남은 공간 차지 */
}

/* 제목 스타일 */
.info-title {
  font-weight: 700;
  font-size: 16px;
  color: #333;
  margin: 0;
}

/* 내용 스타일 */
.info-content {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  padding-left: 10px;
  white-space: nowrap;  /* 줄바꿈 허용 */
  word-break: break-word;  /* 긴 단어 줄바꿈 */
}


/* 2열 레이아웃에서의 각 섹션 */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 0;  /* 그리드 아이템 축소 허용 */
  white-space: nowrap;  /* 줄바꿈 허용 */
}


.description-link {
  display: block;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  /* padding: 12px 0; */
  position: relative;
  transition: color 0.3s ease;
}

.description-link::after {
  content: none; /* 호버 시 나타나는 밑줄 제거 */
}

.description-link:hover {
  color: #0173ba;
}

.description-link:hover::after {
  width: 100%;
}

/* 검색 섹션 */
.search-section {
  margin: 40px 0;
}

/* 검색 섹션 수정 */
.search-header {
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.highlight {
  color: #111111;  /* 더 진한 색상으로 변경 */
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
  letter-spacing: -0.5px;
}

.search-header p {
  color: #666;
  font-size: 15px;
  line-height: 1.6;
}

.search-container {
  position: relative;
  margin-top: 20px;
  max-width: 500px;  /* 검색창 최대 너비 설정 */
}

.search-input {
  width: 100%;
  padding: 15px 20px;
  font-size: 15px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  background-color: #fff;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #0046FF;
  box-shadow: 0 0 0 3px rgba(0, 70, 255, 0.1);
}

/* 질문하기 버튼 위치 조정 */
.create-link {
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  background-color: #8595a9;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 8px;
  text-decoration: none;
  margin-left: auto;  /* 오른쪽 정렬을 위해 추가 */
}

.create-link:hover {
  background-color: #0173ba;
}

/* 게시글 리스트 */
.article-list {
  border: 1px solid #e1e1e1;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  width: 100%;       /* 너비 100% 설정 */
}

.list-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  padding: 16px 24px;
  background-color: #f8f9fd;
  font-weight: 500;
  color: #333;
  border-bottom: 1px solid #e1e1e1;
  text-align: left;  /* 추가 */
}


.list-header span:nth-child(1) {
  text-align: left;
}

.list-header span:nth-child(2) {
  text-align: center;
}

.list-header span:nth-child(3) {
  text-align: center;
}

.list-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;  /* 줄바꿈 방지 */
}

.list-item:hover {
  background-color: #f8f9fd;
}

/* 리스트 아이템의 최소 너비 설정 */
.list-header, .list-item {
  min-width: 100%;   /* 부모 요소의 전체 너비 사용 */
}

.list-title {
  color: #333;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 20px; /* 여유 공간 */
}

.list-nickname {
  color: #666;
  text-align: center;
}

.list-date {
  color: #666;
  text-align: center;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
  padding: 20px 0;
}

.pagination button {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  background-color: #fff;
  border: 1px solid #e1e1e1;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination button:not(:disabled):hover {
  background-color: #0046FF;
  color: white;
  border-color: #0046FF;
}

.pagination button:disabled {
  background-color: #f5f5f5;
  color: #999;
  border-color: #e1e1e1;
}

.pagination span {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* 구분선 진하게 수정 */
.divider {
  border: 0;
  height: 1px;
  background: #d2d2d2;  /* 더 진한 회색으로 변경 */
  margin: 30px 0;
}
</style>