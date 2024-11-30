import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainView from '@/views/MainView.vue'
import FinancialProductsView from '@/views/financial-products/FinancialProductsView.vue'
import DepositProductsView from '@/views/financial-products/DepositProductsView.vue'
import SavingProductView from '@/views/financial-products/SavingProductView.vue'
import ProductDetailView from '@/views/financial-products/ProductDetailView.vue'
import ProductsView from '@/views/financial-products/ProductsView.vue'
import RecommendedProductView from '@/views/financial-products/RecommendedProductView.vue'
import BankRegistrationForm from '@/views/financial-products/BankRegistrationForm.vue'
import SignUpView from '@/views/accounts/SignUpView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import ProfileUpdateView from '@/views/accounts/ProfileUpdateView.vue'
import MapView from '@/views/MapView.vue'
import swal from "sweetalert2";
import ArticleHomeView from '@/views/articles/ArticleHomeView.vue'
import ArticleDetailView from '@/views/articles/ArticleDetailView.vue'
import ArticleCreateView from '@/views/articles/ArticleCreateView.vue'
import ArticleUpdateView from '@/views/articles/ArticleUpdateView.vue'
import GameView from '@/views/game/GameView.vue'


// import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', 
      name: 'MainView',
      component: MainView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
      meta: {requiresAuth: true}   // 인증되지 않은 사용자 접근 제한 
    },
    {
      path: '/profileupdate',
      name: 'ProfileUpdateView',
      component: ProfileUpdateView,
      meta: {requiresAuth: true}   // 인증되지 않은 사용자 접근 제한 
    },
    {
      path: '/financialproducts', 
      name: 'financialproducts',
      component: FinancialProductsView,
      redirect: { name: 'products' },
      children: [
        {
          path: 'products', 
          name: 'products',
          component: ProductsView,
          redirect: { name: 'depositproducts' },
          children: [
            {
              path: 'depositproducts', 
              name: 'depositproducts',
              component: DepositProductsView,
            },
            {
              path: 'savingproducts', 
              name: 'savingproducts',
              component: SavingProductView,
            },
          ]
        },
        {
          path: ':fin_prdt_cd', 
          name: 'productDetail',
          component: ProductDetailView,
          
        },
        {
          path: 'bankregistrationform', 
          name: 'bankregistrationform',
          component: BankRegistrationForm,
        },
        {
          path: 'recommendedproduct', 
          name: 'recommendedproduct',
          component: RecommendedProductView,
        },
      ]
    },
    {
      path: '/map',
      name: 'MapView',
      component: MapView
    },
    {
      path: '/articles',
      name: 'ArticleHomeView',
      component: ArticleHomeView
    },
    {
      path: '/articles/:articleId',
      name: 'ArticleDetailView',
      component: ArticleDetailView,
      meta: {requiresAuth: true} 
    },
    {
      path: '/articles/create/',
      name: 'ArticleCreateView',
      component: ArticleCreateView,
      meta: {requiresAuth: true} 
    },
    {
      path: '/articles/:articleId',
      name: 'ArticleUpdateView',
      component: ArticleUpdateView,
      meta: {requiresAuth: true} 
    },
    {
      path: '/game',
      name: 'GameView',
      component: GameView
    }
  ],
})


router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
    if (to.meta.requiresAuth && !userStore.isLogin) {
      swal.fire({
        title: '로그인이 필요합니다.',
        text: '로그인 후 다시 시도해주세요.',
        icon: 'warning',
      });
      next({ name: 'LoginView' });
    } 

    // 로그인 상태에서 로그인 및 회원가입 페이지 접근 불가
    else if (userStore.isLogin && (to.name === 'LoginView' || to.name === 'SignUpView')) {
      swal.fire({
        title: '이미 로그인하셨습니다.',
        text: '메인 페이지로 이동합니다.',
        icon: 'info',
        timer: 1000,
        showConfirmButton: false,
        width: '400px' // 창의 너비를 400px로 설정
      });
      next({ name: 'MainView' }); // 메인 페이지로 리다이렉트
    } else {
      next(); // 다른 경우에는 그대로 접근 허용
    }
  });


export default router