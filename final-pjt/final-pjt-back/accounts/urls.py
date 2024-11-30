from django.urls import path
from . import views

urlpatterns = [
    # path('signup/', views.signup),
    # path('signout/', views.signout),
    # path('login/', views.login),
    # path('logout/', views.logout),
    path('profile/<str:username>/', views.update_profile),
    path('profile/<str:username>/delete/', views.delete)
]