<template>
  <div class="container">
    <!-- 탭 컨테이너 -->
    <ul class="nav nav-underline">
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'depositproducts' }" 
          class="nav-link" 
          active-class="active"
        >
          예금
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'savingproducts' }" 
          class="nav-link" 
          active-class="active"
        >
          적금
        </RouterLink>
      </li>
    </ul>

    <!-- 콘텐츠 영역 -->
    <div class="tab-content">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
/* 기본 컨테이너 스타일 */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff; /* 하얀 배경 */
  box-sizing: border-box;
}

/* 탭 메뉴 스타일 */
.nav-underline {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0; /* 탭과 콘텐츠 사이 간격 */
}

.nav-item {
  margin-right: 20px;
}

.nav-link {
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  color: #747577;
  padding: 10px 0;
  border-bottom: 2px solid transparent;
  transition: color 0.3s ease, border-bottom 0.3s ease;
}

.nav-link.active {
  color: #2858a6; /* 활성화된 탭의 파란색 */
  border-bottom: 2px solid #2858a6;
}

.nav-link:hover {
  color: #003c82; /* 호버 시 더 어두운 파란색 */
}

/* 콘텐츠 영역 스타일 */
.tab-content {
  margin-top: 20px;
}
</style>
