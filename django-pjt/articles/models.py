# from django.db import models
# from django.conf import settings

# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         default=1  # 기본값으로 사용자 ID 1을 사용
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# from django.db import models
# from django.conf import settings

# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         default=1  # 기본값으로 사용자 ID 1을 사용
#     )
#     rating = models.DecimalField(
#         max_digits=2,  # 최대 자릿수: 정수부 1자리 + 소수부 1자리
#         decimal_places=1,  # 소수부 자릿수
#         null=True,  # 비어 있어도 허용
#         blank=True  # 입력 폼에서 비어 있어도 허용
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# from django.conf import settings
# from django.db import models

# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         default=1  # 기본값으로 사용자 ID 1을 사용
#     )
#     rating = models.DecimalField(
#         max_digits=2,  # 최대 자릿수: 정수부 1자리 + 소수부 1자리
#         decimal_places=1,  # 소수부 자릿수
#         null=True,  # 비어 있어도 허용
#         blank=True  # 입력 폼에서 비어 있어도 허용
#     )
#     liked_users = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,  # 다대다 관계로 사용자와 연결
#         related_name='liked_articles',  # 역참조 이름
#         blank=True  # 비어 있어도 허용
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     @property
#     def likes_count(self):
#         """
#         좋아요 수를 반환하는 속성
#         """
#         return self.liked_users.count()

#     def __str__(self):
#         return f"{self.title} by {self.author.username} ({self.likes_count} likes)"
# from django.conf import settings
# from django.db import models

# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     rating = models.DecimalField(
#         max_digits=2, 
#         decimal_places=1,
#         null=True, 
#         blank=True
#     )
#     liked_users = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='liked_articles',
#         blank=True
#     )

#     @property
#     def likes_count(self):
#         return self.liked_users.count()

# from django.db import models
# from django.conf import settings

# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     rating = models.FloatField(default=0, null=True, blank=True)
#     liked_users = models.ManyToManyField(
#         settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True
#     )

#     @property
#     def likes_count(self):
#         return self.liked_users.count()
from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.FloatField(default=0, null=True, blank=True)
    liked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True
    )

    @property
    def likes_count(self):
        return self.liked_users.count()

    def __str__(self):
        return f"Article: {self.title} by {self.author.username}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=0) & models.Q(rating__lte=5),
                name="rating_range_constraint",
            )
        ]
