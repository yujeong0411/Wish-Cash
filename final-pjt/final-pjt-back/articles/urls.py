from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comments/', views.comments_list),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail),
]