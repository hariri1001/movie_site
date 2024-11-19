from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'), # 회원가입
    path('profile/', views.profile_view, name='profile'),  # 프로필 조회
    path('profile/update/', views.profile_update),  # 프로필 수정
    # path('profile/password/', views.change_password, name='change_password'),
    # path('profile/<int:user_id>/follow/', views.toggle_follow, name='toggle_follow'),
]