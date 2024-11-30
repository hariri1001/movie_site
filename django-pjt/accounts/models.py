from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # 유저가 팔로우 하는 사람들
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.followings.count()


class LikedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.movie.title}'
    

# 영화id와 TMDB의 id 중복 이슈
class Movie(models.Model):
   id = models.IntegerField(primary_key=True)