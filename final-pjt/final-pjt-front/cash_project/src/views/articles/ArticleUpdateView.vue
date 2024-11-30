<template>
  <div class="article-container">
    <!-- 타이틀 -->
    <header class="header">
      <h1>게시글 수정</h1>
    </header>
  
    <!-- 게시글 수정 폼 -->
    <div class="form-description">
      <form @submit.prevent="updateArticle" class="article-form">
        <div class="form-group">
          <label for="form-title">제목</label>
          <input 
            type="text" 
            id="form-title"
            v-model="updatetitle" 
            required
            class="form-input"
          >
        </div>

        <div class="form-group">
          <label for="form-content">내용</label>
          <textarea 
            id="form-content"
            v-model="updatecontent" 
            required
            class="form-textarea"
          ></textarea>
        </div>

        <div class="button-group">
          <button type="submit" class="submit-btn">수정</button>
          <button @click="backArticleHome" type="button" class="cancel-btn">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useArticleStore } from '@/stores/article';
import Swal from 'sweetalert2';
import { useRoute, useRouter } from 'vue-router';

const articleStore = useArticleStore()
const route = useRoute()
const router = useRouter()
const updatetitle = ref('')
const updatecontent = ref('')

// 이전 데이터 
watch(() => 
  articleStore.articleDetail, (pastData) => {
    updatetitle.value = pastData.title
    updatecontent.value = pastData.content
  }
)

const updateArticle = function () {
  Swal.fire({
    title: "게시글을 수정하시겠습니까?",
    icon:"info",
    showCancelButton: true,
    confirmButtonColor: "#2858A6",
    cancelButtonColor: "#828282",
    confirmButtonText: "수정",
    cancelButtonText: "취소",
  }).then((res) => {
    if (res.isConfirmed) {
      const requestData = {
        title: updatetitle.value,
        content: updatecontent.value,
        articleId: route.params.articleId
      }
      articleStore.updateArticle(requestData)
      Swal.fire("수정되었습니다.")
    }
  })
}


// 취소 버튼
const backArticleHome = function () {
  router.push({name:'ArticleDetailView'})
}

onMounted(() => {
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

/* 폼 컨테이너 */
.form-description {
  background: linear-gradient(145deg, #f8f9fd 0%, #f2f4f8 100%);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  font-size: 15px;
  background-color: white;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #0046FF;
  box-shadow: 0 0 0 3px rgba(0, 70, 255, 0.1);
}

.form-textarea {
  min-height: 300px;
  resize: vertical;
}

/* 버튼 그룹 */
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.submit-btn,
.cancel-btn {
  padding: 12px 24px;
  font-size: 15px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.submit-btn {
  background-color: #8595a9;
  color: white;
}

.submit-btn:hover {
  background-color: #003ACC;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 70, 255, 0.3);
}

.cancel-btn {
  background-color: #8595a9;
  color: white;
}

.cancel-btn:hover {
  background-color: #003ACC;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 70, 255, 0.3);
}
</style>