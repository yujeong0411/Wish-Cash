from django.urls import path
from . import views

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    path('deposit-options/<str:fin_prdt_cd>/', views.deposit_options),
    path('save-saving-products/', views.save_saving_products),
    path('saving-products/', views.saving_products),
    path('saving-options/<str:fin_prdt_cd>/', views.saving_options),
    path('save-exchange/', views.save_exchange),
    path('exchange/', views.exchange),
    path('api/chatbot/', views.ChatBotAPIView.as_view()),
    path('subscribed/', views.subscribed),
    path('subscribed-list/', views.subscribed_list),
    path('unsubscribe/', views.unsubscribe),
    path('similar-age-products/', views.get_similar_age_products),
]