<script setup>
import { ref, onMounted } from 'vue'
import { useMapStore } from '@/stores/map.js'
import { storeToRefs } from 'pinia'

const store = useMapStore()
const { bankList, searchKeyword } = storeToRefs(store)
const isSidebarOpen = ref(true) // 은행 목록과 검색창의 열림/닫힘 상태

onMounted(() => {
  store.initializeMap()
})

// 은행 목록 열고 닫기
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>

<template>
  <div class="map-wrapper">
    <!-- 목록 및 검색창 (왼쪽 NAV) -->
    <div class="sidebar" :class="{ open: isSidebarOpen }">
      <div class="sidebar-content">
        <!-- 검색 영역 -->
        <div class="search-container">
          <input 
            type="text" 
            @keyup.enter="store.searchByKeyword" 
            placeholder="은행명 또는 지역명을 입력하세요" 
            v-model="searchKeyword"
            class="search-input">
          <button 
            type="button" 
            @click="store.searchByKeyword"
            class="search-button">
            검색
          </button>
        </div>
        <!-- 검색 결과 -->
        <div class="results-container">
          <p class="results-count">근처에 총 {{ bankList.length }} 개의 은행이 있습니다.</p>
          <hr>
          <div v-for="(bank, index) in bankList" :key="bank.id" class="bank-item">
            <p><strong class="highlight">{{ bank.place_name }}</strong></p>
            <ul class="bank-details">
              <li v-if="bank.phone">전화: {{ bank.phone }}</li>
              <li v-if="bank.road_address_name">주소: {{ bank.road_address_name }}</li>
              <li><a :href="bank.place_url" target="_blank">상세보기</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- 지도 -->
    <div id="map" class="map-container" :class="{ 'full-width': !isSidebarOpen }"></div>

    <!-- 화살표 버튼 -->
    <button class="sidebar-toggle" @click="toggleSidebar">
      <span v-if="isSidebarOpen">&lt;</span>
      <span v-else>&gt;</span>
    </button>
  </div>
</template>


<style scoped>
.divder {
  
}
/* 지도와 사이드바 컨테이너 */
.map-wrapper {
  display: flex;
  width: 100%;
  height: 100vh; /* 화면 전체 높이 */
  position: relative;
  transition: all 0.3s ease;
}

/* 지도 스타일 */
.map-container {
  flex: 1; /* 기본적으로 남은 공간을 모두 차지 */
  height: 100%;
  background-color: #f0f0f0;
  transition: all 0.3s ease; /* 지도가 확장될 때 부드럽게 변화 */
}

.map-container.full-width {
  flex: 1 0 100%; /* 지도 영역이 전체를 차지하도록 확장 */
}

/* 사이드바 (왼쪽 NAV) */
.sidebar {
  width: 300px;
  background-color: #ffffff;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.2);
  height: 100%;
  overflow-y: auto;
  transition: all 0.3s ease;
  z-index: 1000;
}

.sidebar.open {
  transform: translateX(0);
}

.sidebar:not(.open) {
  width: 0; /* 사이드바의 넓이를 0으로 줄여 숨김 */
  transform: translateX(-100%);
}

/* 사이드바 내용 */
.sidebar-content {
  padding: 20px;
  overflow-y: auto;
}

/* 화살표 버튼 */
.sidebar-toggle {
  position: absolute;
  top: 50%;
  left: 300px; /* 사이드바가 열려있을 때의 위치 */
  width: 20px;
  height: 50px;
  background-color: #727374;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
  transform: translateY(-50%);
  z-index: 1100;
  transition: all 0.3s ease; /* left 대신 all을 사용하여 모든 변화에 트랜지션 적용 */
}

.sidebar-toggle:hover {
  background-color: #042b52;
}

/* 사이드바가 닫혔을 때의 버튼 위치 */
.sidebar:not(.open) ~ .sidebar-toggle {
  left: 0; /* 완전히 왼쪽으로 이동 */
}

/* 검색 영역 */
.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 3px;
  height: 30px;
  border: 1px solid #dcdcdc;
  border-radius: 4px;
  font-size: 14px;
}

.search-button {
  display: flex;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  padding: 0 20px; /* 상하 padding을 제거 */
  background-color: #727374;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px; /* 글자 크기 */
  transition: background-color 0.3s;
  height: 35px; /* 버튼 높이 */
  text-align: center; /* 텍스트 중앙 정렬 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

button:hover {
  opacity: 0.9;
}

/* 검색 결과 */
.results-container {
  margin-top: 20px;
}

.results-count {
  font-size: 14px;
  color: #333;
  margin-bottom: 10px;
}

.bank-item {
  padding: 15px 0;
  border-bottom: 1px solid #ddd;
}

.bank-item h5 {
  color: #2858A6;
}

.bank-details {
  list-style: none;
  padding: 0;
  margin: 0;
}

.bank-details li {
  font-size: 14px;
  color: #666;
  margin: 5px 0;
}

.bank-details a {
  color: #2858A6;
  text-decoration: none;
}

.bank-details a:hover {
  text-decoration: underline;
}

.highlight {
  color: #19549c;
}
</style>
