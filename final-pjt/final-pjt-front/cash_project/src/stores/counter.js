import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

export const useCounterStore = defineStore('counter', () => {
  const depositproducts = ref([])
  const depositoptions = ref([])
  const savingproducts = ref([])
  const savingoptions = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const saveDepositProducts = function() {
    axios({
      method: 'get',
      url: `${API_URL}/finance/save-deposit-products/`
    }).then(res => {
      depositproducts.value = res.data
      getDepositProducts()
    }).catch(err => console.log(err))
  }
  
  const getDepositOptions = async function(fin_prdt_cd) {
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/finance/deposit-options/${fin_prdt_cd}/`,
      });
      return res.data; // 데이터 반환
    } catch (err) {
      console.error(err);
      return []; // 오류 시 빈 배열 반환
    }
  };

  const getDepositProducts = async function() {
    try {
      depositoptions.value = []; // 초기화
      const res = await axios({
        method: 'get',
        url: `${API_URL}/finance/deposit-products/`
      });
  
      depositproducts.value = res.data;
      depositoptions.value = []
  
      for (const depositproduct of depositproducts.value) {
        const options = await getDepositOptions(depositproduct.fin_prdt_cd);
  
        let baseRate = null, baseTrm = null, maxRate = null, maxTrm = null;
  
        for (const option of options) {
          if ([1, 3, 6, 12].includes(option.save_trm)) {
            baseRate = option.intr_rate;
            baseTrm = option.save_trm;
          }
          if (option.intr_rate2 > (maxRate || -Infinity)) {
            maxRate = option.intr_rate2;
            maxTrm = option.save_trm;
          }
        }
  
        depositproduct['base_rate'] = baseRate;
        depositproduct['base_trm'] = baseTrm;
        depositproduct['max_rate'] = maxRate;
        depositproduct['max_trm'] = maxTrm;
        depositproduct['options'] = options;
        depositproduct['kor_co_nm'] = depositproduct.kor_co_nm || 'Unknown Bank';
  
        depositoptions.value.push(depositproduct);
      }
    } catch (err) {
      console.error(err);
      alert('An error occurred while fetching deposit products.');
    }
  };  

  const saveSavingProducts = function() {
    axios({
      method: 'get',
      url: `${API_URL}/finance/save-saving-products/`
    }).then(res => {
      savingproducts.value = res.data
      getSavingProducts()
    }).catch(err => console.log(err))
  }
  
  const getSavingOptions = async function(fin_prdt_cd) {
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/finance/saving-options/${fin_prdt_cd}/`,
      });
      return res.data; // 데이터 반환
    } catch (err) {
      console.error(err);
      return []; // 오류 시 빈 배열 반환
    }
  };

  const getSavingProducts = async function() {
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/finance/saving-products/`
      });
  
      savingproducts.value = res.data; // savingproducts.value에 데이터를 할당
      savingoptions.value = []

      for (const savingproduct of savingproducts.value) {
        const options = await getSavingOptions(savingproduct.fin_prdt_cd); // await 추가
      
        // 초기값 설정
        let baseRate = null; // 기준 금리 초기값
        let baseTrm = null;
        let maxRate = null; // 최고 금리 초기값
        let maxTrm = null;
      
        // 옵션 순회
        for (const option of options) {
          // 기준 금리 조건
          if ([1, 3, 6, 12].includes(option.save_trm)) {
            baseRate = option.intr_rate;
            baseTrm = option.save_trm;
          }
  
          // 최고 금리 조건
          if (option.intr_rate2 > (maxRate || -Infinity)) {
            maxRate = option.intr_rate2;
            maxTrm = option.save_trm;
          }
        }
      
        // 결과 객체 생성
        savingproduct['base_rate'] = baseRate !== null ? baseRate : null;
        savingproduct['base_trm'] = baseTrm !== null ? baseTrm : null;
        savingproduct['max_rate'] = maxRate !== null ? maxRate : null;
        savingproduct['max_trm'] = maxTrm !== null ? maxTrm : null;
        savingproduct['options'] = options; // 옵션 저장
      
        // 은행명을 포함하는 속성 추가
        savingproduct['kor_co_nm'] = savingproduct.kor_co_nm || 'Unknown Bank';
      
        savingoptions.value.push(savingproduct); // 결과 저장
      }
    } catch (err) {
      console.error(err);
    }
  };

  const allDepositProducts = ref([]);
  const allSavingProducts = ref([]);
  const similarAgeDepositProducts = ref([]);
  const similarAgeSavingProducts = ref([]);

  const fetchProducts = async (userAge) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/finance/similar-age-products/", {
        params: { age: userAge },
      });

      const data = response.data.data;

      // 제품 데이터 업데이트
      allDepositProducts.value = data.top_all_deposit_products;
      allSavingProducts.value = data.top_all_saving_products;
      similarAgeDepositProducts.value = data.top_similar_age_deposit_products;
      similarAgeSavingProducts.value = data.top_similar_age_saving_products;
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };
  
  const exchange = ref([])

  const saveExchange = function() {
    axios({
      method: 'get',
      url: `${API_URL}/finance/save-exchange/`
    }).then(res => {
      getExchange()
    }).catch(err => console.log(err))
  }

  const getExchange = function() {
    axios({
      method: 'get',
      url: `${API_URL}/finance/exchange/`
    }).then(res => {
      exchange.value = res.data
    }).catch(err => console.log(err))
  }

  const fetchAndSaveStockData = function() {
    axios({
        method: 'get',
        url: `${API_URL}/game/fetch-and-save-stock-data/`
    }).then(res => {
        console.log('성공:', res.data); // 응답 데이터 출력
    }).catch(err => {
        console.error('오류 발생:', err.message);
        if (err.response) {
            // 서버가 응답했지만 상태 코드가 2xx가 아닌 경우
            console.error('응답 데이터:', err.response.data);
            console.error('상태 코드:', err.response.status);
        } else if (err.request) {
            // 요청이 전송되었으나 응답이 없을 경우
            console.error('요청 데이터:', err.request);
        } else {
            // 요청 설정 중에 오류가 발생한 경우
            console.error('요청 설정 오류:', err.message);
        }
    });
}

  return { 
    saveDepositProducts,
    saveSavingProducts,
    getDepositProducts, 
    getDepositOptions, 
    getSavingProducts, 
    getSavingOptions,
    fetchProducts,
    saveExchange,
    getExchange, 
    fetchAndSaveStockData,
    depositproducts,
    depositoptions,
    savingproducts,
    savingoptions,
    allDepositProducts,
    allSavingProducts,
    similarAgeDepositProducts,
    similarAgeSavingProducts,
    exchange,
  }
}, {persist: true})
