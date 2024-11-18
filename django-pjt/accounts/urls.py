from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    # path('profile/password/', views.change_password, name='change_password'),
    # path('profile/<int:user_id>/follow/', views.toggle_follow, name='toggle_follow'),
]