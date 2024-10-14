
from django.urls import path

from cases.views import transcribed_cases_count

from .views import SignupView, LoginView, UserDetailView, UserListView, ProfileListView,ProfileView
from . import views
urlpatterns = [
    path('signup/', SignupView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileView.as_view(), name='profile_list'),
    path('generate_token/', views.generate_token, name='generate_token'),
    path('transcribed-cases/', transcribed_cases_count, name='transcribed-cases'),
]