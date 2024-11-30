<template>
  <div class="chat-container">
    <header>
      <h1>금융상담 챗봇</h1>
      <p class="subtitle">금융 관련 궁금한 점을 물어보세요!</p>
    </header>

    <!-- 채팅 기록 표시 -->
    <div class="chat-history" ref="chatHistoryRef">
      <div
        v-for="(message, index) in chatHistory"
        :key="index"
        :class="['message', message.role]"
      >
        <div class="message-bubble">
          <div class="message-header">
            <span class="avatar">
              {{ message.role === 'user' ? '👤' : '🤖' }}
            </span>
            {{ message.role === 'user' ? '나' : 'WishCash Bot' }}
          </div>
          <div class="message-content">
            {{ message.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- 사용자 입력 -->
    <form @submit.prevent="sendMessage" class="input-form">
      <div class="input-wrapper">
        <textarea
         class="chatbot-input"
          v-model="userQuery"
          placeholder="질문을 입력해주세요..."
          @keypress.enter.prevent="sendMessage"
        ></textarea>
        <button type="submit" :disabled="isLoading || !userQuery.trim()">
          {{ isLoading ? '답변 중...' : '전송' }}
        </button>
      </div>
    </form>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error-message">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter.js'

const API_URL = 'http://127.0.0.1:8000';
const store = useCounterStore()

// 스토어에서 필요한 데이터 가져오기
const depositProducts = store.depositproducts;
const depositOptions = store.depositoptions;
const savingProducts = store.savingproducts;
const savingOptions = store.savingoptions;
const allDepositProducts = store.allDepositProducts;
const allSavingProducts = store.allSavingProducts;
const similarAgeDepositProducts = store.similarAgeDepositProducts;
const similarAgeSavingProducts = store.similarAgeSavingProducts;
const exchange = store.exchange;

// 사전 데이터: 시스템 메시지로 포함할 데이터
const systemMessages = [
  {
    role: "system", 
    content: JSON.stringify({
      role: "expert",
      domain: "finance",
      instructions: "당신은 금융 전문가입니다. 사용자에게 금융 관련 정보를 친절하고 정확하게 제공합니다.",
      depositProducts,
      depositOptions,
      savingProducts,
      savingOptions,
      // allDepositProducts,
      // allSavingProducts,
      // similarAgeDepositProducts,
      // similarAgeSavingProducts,
      // exchange
    })
  },
];

// 나머지 코드
const userQuery = ref('');
const chatHistory = ref([]);
const isLoading = ref(false);
const error = ref('');
const chatHistoryRef = ref(null);

// 채팅 기록 자동 스크롤
watch(chatHistory, async () => {
  await nextTick();
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight;
  }
}, { deep: true });

// 메시지 전송
const sendMessage = async () => {
  if (!userQuery.value.trim() || isLoading.value) return;
  
  const currentQuery = userQuery.value;
  userQuery.value = '';
  isLoading.value = true;
  error.value = '';
  
  // 사용자 메시지를 채팅 기록에 추가 (UI에 표시)
  chatHistory.value.push({ role: 'user', content: currentQuery });
  
  try {
    // 시스템 메시지와 사용자 메시지를 결합하여 백엔드로 전송
    const response = await axios.post(`${API_URL}/finance/api/chatbot/`, {
      message: currentQuery,
      chat_history: [...systemMessages, ...chatHistory.value], // 시스템 메시지를 포함
    });
    
    // 서버에서 반환된 봇 응답을 UI에 추가
    chatHistory.value.push({
      role: 'assistant',
      content: response.data.reply,
    });
  } catch (err) {
    console.error("Error:", err);
    error.value = 'An error occurred. Please try again.';
    chatHistory.value.push({
      role: 'assistant',
      content: '죄송합니다. 요청 처리 중 오류가 발생했습니다.',
    });
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fbfbfb;
  border-radius: 12px;
}

header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #615c5c;
}

header h1 {
  font-size: 28px;
  color: #000000;
  margin: 0;
  padding-bottom: 8px;
}

.subtitle {
  color: #4f4d4d;
  font-size: 14px;
  margin: 0;
}

.message {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message-bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.user .message-bubble {
  background-color: #2858A6;
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant .message-bubble {
  background-color: #f0f2f5;
  color: #1c1e21;
  border-bottom-left-radius: 4px;
}

.message-header {
  font-size: 12px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.user .message-header {
  color: #e3e3e3;
}

.assistant .message-header {
  color: #65676b;
}

.avatar {
  font-size: 16px;
}

.message-content {
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
}

.input-wrapper {
  display: flex;
  gap: 10px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #eee;
}

textarea {
  flex: 1;
  height: 50px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: none;
  font-size: 14px;
  background-color: white;
  transition: border-color 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #0173BA;
}

button {
  padding: 0 20px;
  background-color: #0173BA;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
  min-width: 80px;
}

button:hover:not(:disabled) {
  background-color: #075789;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 10px;
  padding: 10px;
  background-color: #fef2f2;
  color: #dc2626;
  border-radius: 6px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-icon {
  font-size: 16px;
}

/* 스크롤바 스타일링 */
.chat-history {
  min-height: 100px;  /* 최소 높이 설정 */
  max-height: 500px;  /* 최대 높이 설정 */
  overflow-y: auto;   /* 내용이 넘칠 때만 스크롤 표시 */
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.chat-history::-webkit-scrollbar {
  width: 6px;
}

.chat-history::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-history::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-history::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
