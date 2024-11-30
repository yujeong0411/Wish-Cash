<template>
  <div class="article-container">
    <!-- 타이틀 -->
    <header class="header">
      <h1>자주하는 질문</h1>
      <div class="header-buttons">
        <button class="icon-btn" @click="handleShare">
          <i class="fas fa-share-alt"></i>
        </button>
        <button class="icon-btn" @click="handlePrint">
          <i class="fas fa-print"></i>
        </button>
      </div>
    </header>

    <!-- 게시글 내용 -->
    <div class="article-content-box"   v-if="articleStore.articleDetail && userStore.userInfo">
      <div class="article-header">
        <div class="qa-section">
          <div class="qa-icon q-icon">Q</div>
          <h2 class="article-title">{{ articleStore.articleDetail.title }}</h2>
        </div>
        <div class="button-group" v-if= "articleStore.articleDetail && articleStore.articleDetail.user && articleStore.articleDetail.user.username === userStore.userInfo.username">
          <button @click="articleUpdate" class="edit-btn">수정</button>
          <button @click="articleDelete" class="delete-btn">삭제</button>
        </div>
      </div>

      <div class="article-body">
        <div class="qa-section">
          <div class="qa-icon a-icon">A</div>
          <p class="article-text">{{ articleStore.articleDetail.content }}</p>
        </div>
      </div>

      <div class="article-footer">
        <div class="date-info">
          <div class="date-item">
            <span class="date-label">작성일:</span>
            <span class="date-value">
              {{ formatDate(articleStore.articleDetail.created_at) }}
              {{ formatTime(articleStore.articleDetail.created_at) }}
            </span>
          </div>
          <div class="date-item">
            <span class="date-label">수정일:</span>
            <span class="date-value">
              {{ formatDate(articleStore.articleDetail.updated_at) }}
              {{ formatTime(articleStore.articleDetail.updated_at) }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <!-- 댓글목록 -->
    <div v-if="articleStore.articleDetail && userStore.userInfo">
      <!-- {{ articleStore.articleDetail }} -->
      <Comments :username="userStore.userInfo.username" :articleuser="articleStore.articleDetail.user.username" />
    </div>

    <!-- 목록 버튼 추가 -->
    <div class="list-button-container">
      <button @click="backArticleHome" class="list-button">목록</button>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useArticleStore } from '@/stores/article';
import { useUserStore } from '@/stores/user';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { format, parseISO } from "date-fns";
import Swal from 'sweetalert2';
import Comments from '@/components/Comments.vue';


const articleStore = useArticleStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const articleUpdate = function () {
  router.push({name:'ArticleUpdateView', params:{articleId:articleStore.articleDetail.id}})
}

const articleDelete = function () {
  Swal.fire({
    title: "게시글을 삭제하시겠습니까?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#2858A6",
    cancelButtonColor: "#828282",
    confirmButtonText: "삭제",
    cancelButtonText: "취소",
  }).then((res) => {
    if (res.isConfirmed) {
      articleStore.deleteArticle(articleStore.articleDetail.id)
      Swal.fire({
        title:"게시글이 삭제되었습니다.",
        icon:"success"
      })
    } else {
      Swal.fire({
        title:"취소되었습니다."
      })
    }
  })
}

// 날짜, 시간 변환
const formatDate = (dateString) => {
  return format(parseISO(dateString), "yyyy-MM-dd");
};

const formatTime = (dateString) => {
  return format(parseISO(dateString), "HH:mm:ss");
};

// 목록 버튼
const backArticleHome = function () {
  router.push({name:'ArticleHomeView'})
}

// 게시글 불러오기
onMounted(() => {
  console.log(route.params)
  articleStore.getArticleDetail(route.params.articleId)
})

</script>

<style scoped>
/* 전체 컨테이너 */
.article-container {
 width: 100%;
 min-width: 800px;
 max-width: 1200px;
 margin: 0 auto;
 padding: 40px 20px;
 background-color: #ffffff;
 box-sizing: border-box;
 font-family: 'Noto Sans KR', sans-serif;
 overflow-x: auto;
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

/* 게시글 콘텐츠 박스 */
.article-content-box {
 /* background: linear-gradient(145deg, #f8f9fd 0%, #f2f4f8 100%); */
 /* border-radius: 12px; */
 padding: 30px;
 margin-bottom: 40px;
 /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); */
}

/* 게시글 헤더 */
.article-header {
 display: flex;
 justify-content: space-between;
 align-items: flex-start;
 margin-bottom: 30px;
 padding-bottom: 20px;
 border-bottom: 1px solid #e1e1e1;
}

.article-title {
 font-size: 24px;
 font-weight: 700;
 color: #111111;
 margin: 0;
}

/* 버튼 그룹 */
.button-group {
 display: flex;
 gap: 10px;
}

.edit-btn,
.delete-btn {
 padding: 8px 16px;
 font-size: 14px;
 font-weight: 500;
 border-radius: 8px;
 cursor: pointer;
 transition: all 0.3s ease;
 border: none;
 color: white;
}

button:hover {
  opacity: 0.9;
}

.edit-btn {
  background-color: #0173ba;
}

.delete-btn {
 background-color: #8595a9;
}

/* 게시글 본문 */
.article-body {
 margin-bottom: 30px;
 padding: 20px 0;
}

.article-text {
 font-size: 16px;
 line-height: 1.6;
 color: #333;
 white-space: pre-wrap;
}

/* 게시글 푸터 */
.article-footer {
 padding-top: 20px;
 border-top: 1px solid #e1e1e1;
 display: flex;
  justify-content: flex-end; /* 푸터 전체를 오른쪽으로 정렬 */
}

.date-info {
 display: flex;
 flex-direction: row;
 gap: 20px;
}

.date-item {
 display: flex;
 align-items: center;
 color: #666;
 font-size: 12px;
}

.date-label {
 font-weight: 500;
 margin-right: 5px; /* 텍스트와 날짜 사이 간격을 줄임 */
}

.date-value {
 color: #888;
 margin-left: 0; /* 불필요한 왼쪽 간격 제거 */
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.icon-btn {
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  padding: 5px;
}

.qa-section {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.qa-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  flex-shrink: 0;
}

.q-icon {
  background-color: #4e85f4;
  color: white;
}

.a-icon {
  background-color: #8595a9;
  color: white;
}

.article-title {
  font-size: 24px;
  font-weight: 700;
  color: #111111;
  margin: 0;
  padding-top: 5px;
}

.article-text {
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  white-space: pre-wrap;
  margin: 0;
  padding-top: 5px;
}

/* 목록 버튼 스타일 */
.list-button-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding-bottom: 20px;
}

.list-button {
  padding: 12px 40px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  background-color: #8595a9;
  color: white;
}

.list-button:hover {
  background-color: #666b76;
}


</style>