from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # 유저가 팔로우 하는 사람들
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.followings.count()


class LikedMovie(models.Model):
    # LikedMovie 모델은 User와 Movie 간의 관계를 나타냄
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)  # 'movies.Movie'로 문자열 참조
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.movie.title}'  # LikedMovie 인스턴스의 문자열 표현 추가
    
    
class Movie(models.Model):
   id = models.IntegerField(primary_key=True)