<template>
  <div>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';

</script>

<style scoped>
/* 페이지 제목 스타일 */
.page-title {
  font-size: 42px; /* 제목 글씨 더 크게 */
  font-weight: bold;
  color: #326ECF;
  text-align: left; /* 왼쪽 정렬 */
  margin-bottom: 20px;
  margin-left: 20px; /* 왼쪽 여백 */
}

/* 탭 컨테이너 스타일 */
.tabs-container {
  display: flex;
  justify-content: center;
  gap: 0; /* 탭 간격 제거 */
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px; /* 테두리 둥글게 */
  overflow: hidden; /* 테두리 안쪽 탭 잘림 방지 */
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

/* 탭 스타일 */
.tab {
  padding: 15px 50px; /* 기존 탭 크기 유지 */
  text-decoration: none;
  font-weight: bold;
  font-size: 18px;
  color: #326ECF;
  border-right: 1px solid #ddd;
  text-align: center;
  flex: 1;
  background-color: white;
}

.tab:last-child {
  border-right: none;
}

.tab:hover {
  background-color: #f0f0f0;
}

/* 활성화된 탭 스타일 */
.active-tab {
  background-color: #326ECF;
  color: white;
}
</style>
