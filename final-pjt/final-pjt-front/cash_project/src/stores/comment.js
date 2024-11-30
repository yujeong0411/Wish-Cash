import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

export const useCommentStore = defineStore("comment", () => {
  const userStore = useUserStore()
  const comments = ref([])
  const API_URL = 'http://127.0.0.1:8000/articles'

  // 댓글 조회
  const getCommentList = function (articleId) {
    axios({
      method: 'get',
      url:`${API_URL}/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${userStore.token}`,
      }
    }).then((res) => {
      console.log(res, "댓글 조회 성공")
      comments.value = res.data
    }).catch((err) => {
      console.log(err, "댓글 조회 실패")
    })
  }


  // 댓글 생성
  const createComment = function (requestData) {
    const { articleId, content } = requestData
    axios({
      method:'post',
      url:`${API_URL}/${articleId}/comments/`,
      data: {
        content
      },
      headers: {
        Authorization: `Token ${userStore.token}`,
      }
    }).then((res) => {
      console.log(res, "댓글 생성 성공")
      comments.value.push(res.data)
    }).catch((err) => {
      console.log(err, "댓글 생성 실패")
    })
  }


  // 댓글 수정
  const updateComment = function (articleId, commentId, content) {
    axios({
      method: 'put',
      url:`${API_URL}/${articleId}/comments/${commentId}/`,
      data: {
        content
      },
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    }).then((res) => {
      console.log(res, "댓글 수정 성공")
      getCommentList(articleId)  // 댓글 목록 다시 불러오기
    }).catch((err) => {
      console.log(err, "댓글 수정 실패")
    })
  }


  // 댓글 삭제
  const deleteComment = function (articleId, commentId) {
    axios({
      method:'delete',
      url:`${API_URL}/${articleId}/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    }).then((res) => {
      console.log(res, "댓글 삭제 성공")
      getCommentList(articleId)
    }).catch((err) => {
      console.log(err, "댓글 삭제 실패")
    })
  }

  return {
    comments, 
    getCommentList, 
    createComment, 
    updateComment, 
    deleteComment,
  }
}, {persist:true})