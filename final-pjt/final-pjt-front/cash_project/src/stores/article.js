import { defineStore } from 'pinia';
import { ref } from 'vue';
import  axios  from 'axios';
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router';
import swal from 'sweetalert2'

export const useArticleStore = defineStore('article', () => {
  const userStore = useUserStore()
  const API_URL = 'http://127.0.0.1:8000'
  const articleList = ref([])
  const articleDetail = ref(null)
  const router = useRouter()

  // 게시글 조회
  const getArticleList = function () {
    axios({
      method: 'get',
      url:`${API_URL}/articles/`,
      headers: {
        Authorization: `Token ${userStore.token}`,
      }
    }).then((res) => {
      console.log(res.data, "게시글 조회 성공")
      articleList.value = res.data
    }).catch((err) => {
      console.log(err, "게시글 조회 실패")
    })
  }


// 게시글 디테일
const getArticleDetail = function (articleId) {
  axios({
    method: 'get',
    url:`${API_URL}/articles/${articleId}/`,
    headers: {
      Authorization : `Token ${userStore.token}`
    }
  }).then((res) => {
    articleDetail.value = null
    console.log(res, "게시글 디테일 성공")
    articleDetail.value = res.data
  }).catch((err) => {
    console.log(err, "게시글 디테일 실패")
  })
}

// 게시글 생성
const createArticle = function (requestData) {
  const { title, content } = requestData
  axios({
    method:'post',
    url:`${API_URL}/articles/`,
    data: {
      title :title,
      content:content
    },
    headers: {
      Authorization : `Token ${userStore.token}`
    }
  }).then((res) => {
    console.log(res, "게시글 생성 성공")
    router.push({name:"ArticleDetailView", params:{articleId:res.data.id}})
  }).catch((err) => {
    console.log(err, "게시글 생성 실패")
  })
}


// 게시글 삭제
const deleteArticle = function (articleId) {
  axios({
    method:'delete',
    url:`${API_URL}/articles/${articleId}/`,
    headers: {
      Authorization : `Token ${ userStore.token }`
    }
  }).then((res) =>{
    console.log(res, "게시글 삭제 성공")
    router.push({name:"ArticleHomeView"})
  }).catch((err) => {
    console.log(err, "게시글 삭제 실패")
  })
}


// 게시글 수정
const updateArticle = function (requestData) {
  const { title, content, articleId } = requestData
  axios({
    method:'put',
    url:`${API_URL}/articles/${articleId}/`,
    data: {
      title,
      content,
      articleId
    },
    headers: {
      Authorization : `Token ${ userStore.token }`
    }
  }).then((res) => {
    console.log(res)
    swal.fire({
      title: "수정이 완료되었습니다.",
      icon:"success"
    })
    router.push({name:"ArticleDetailView", params:{articleId:articleId}})
  }).catch((err) => {
    console.log(err, "게시글 수정 실패")
  })
}
  return {
    articleList,
    articleDetail,
    getArticleList,
    getArticleDetail,
    createArticle,
    updateArticle,
    deleteArticle,
  }
}, {persist:true})