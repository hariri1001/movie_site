from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) # 작성자
    rating = models.FloatField(default=0, null=True, blank=True) # 평점
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.liked_users.count()

    def __str__(self):
        return f"Article: {self.title} by {self.author.username}"

    class Meta: # 평점에 대한 제약 조건 검사 (5점 이상이되는것을 방지)
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=0) & models.Q(rating__lte=5),
                name="rating_range_constraint",
            )
        ]
