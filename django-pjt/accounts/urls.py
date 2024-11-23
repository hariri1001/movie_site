from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'), # 회원가입
    path('profile/', views.profile_view, name='profile'),  # 프로필 조회
    path('profile/update/', views.profile_update),  # 프로필 수정
    path('delete/', views.delete_account, name='delete'), # 회원 탈퇴
    path('profile/image/', views.profile_image_upload, name='profile-image-upload'), # 프로필 이미지 업로드
    path('profile/<str:username>/', views.user_profile, name='user-profile'),  # 특정 사용자 프로필 조회
    path('follow/<str:username>/', views.toggle_follow, name='toggle-follow'),  # 팔로우/언팔로우

]