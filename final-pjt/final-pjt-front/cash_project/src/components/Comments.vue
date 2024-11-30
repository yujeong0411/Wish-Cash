<template>
  <!-- 댓글 작성 폼 -->
  <div class="comment-form-container">
    <form @submit.prevent="newComment" class="comment-form">
      <input 
        type="text"
        v-model="comment"
        placeholder="의견을 나누어보세요."
        class="comment-input"
      >
      <button type="submit" class="submit-btn">작성</button>
    </form>
  </div>
  
  <!-- 댓글 목록 -->
  <div v-if="commentList.length" class="comments-container">
    <div v-for="comment in commentList" :key="comment.id" class="comment-item">
      <!-- 일반 모드 -->
      <div v-if="editCommentId !== comment.id" class="comment-content">
        <div class="comment-header">
          <span class="user-name">{{ comment.user.nickname }}</span>
          <div v-if="userStore.userInfo.username === comment.user.username" class="comment-actions">
            <button @click="startEdit(comment)" class="edit-btn">수정</button>
            <button @click="deleteComment" :value="comment.id" class="delete-btn">삭제</button>
          </div>
        </div>
        <p class="comment-text">{{ comment.content }}</p>
      </div>
      <!-- 수정 모드 -->
      <div v-else class="edit-mode">
        <input 
          type="text"
          v-model="editContent"
          class="edit-input"
          @keyup.enter="saveEdit(comment.id)"
          @keyup.esc="cancelEdit"
        >
        <div class="edit-actions">
          <button @click="saveEdit(comment.id)" class="save-btn">저장</button>
          <button @click="cancelEdit" class="cancel-btn">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores/user";
import { useCommentStore } from "@/stores/comment";

defineProps({
  username: String,
  articleuser: String
})

const route = useRoute()
const userStore = useUserStore()
const commentStore = useCommentStore()
const comment = ref('')
const commentList = ref([])
const editCommentId = ref(null)
const editContent = ref('')

// 댓글 조회
const getCommentList = function () {
  commentStore.getCommentList(route.params.articleId)
}

watch(() => commentStore.comments, (newComment) => {
  commentList.value = newComment
})

// 댓글 생성
const newComment = function () {
  if (comment.value.trim()) {
    const requestData = {
      articleId: route.params.articleId,
      content: comment.value
    }
    commentStore.createComment(requestData)
    comment.value = '' // 초기화 
  }
}

// 댓글 수정 시작
const startEdit = (comment) => {
  editCommentId.value = comment.id
  editContent.value = comment.content
}

// 댓글 수정 저장
const saveEdit = (commentId) => {
  if (editContent.value.trim()) {
    commentStore.updateComment(route.params.articleId, commentId, editContent.value)
    editCommentId.value = null
    editContent.value = ''
  }
}

// 댓글 수정 취소
const cancelEdit = () => {
  editCommentId.value = null
  editContent.value = ''
}

// 댓글 삭제
const deleteComment = function (event) {
  commentStore.deleteComment(route.params.articleId, event.target.value)
}

onMounted(() => {
  getCommentList()
})
</script>

<style scoped>
.comments-container {
  margin: 20px 0;
}

.comment-item {
  padding: 15px;
  border-bottom: 1px solid #e1e1e1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.comment-text {
  color: #666;
  margin: 0;
}

.comment-actions {
  display: flex;
  gap: 8px;
}

.edit-btn,
.delete-btn,
.save-btn,
.cancel-btn {
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  color: white;
}

.edit-btn {
  background-color: #0173ba;
}

.delete-btn {
  background-color: #8595a9;
}

.save-btn {
  background-color: #0173ba;
}

.cancel-btn {
  background-color: #8595a9;
}

.edit-mode {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.edit-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}


/* 입력창 반응형으로 둘지?? */
.comment-form-container {
  margin-top: 10px;
 
}

.comment-form {
  display: flex;
  gap: 10px;
}

.comment-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.submit-btn {
  padding: 8px 16px;
  background-color: #0173ba;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}
</style>