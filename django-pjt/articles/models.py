from django.db import models

# Create your models here.
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)  # 게시글 제목
    content = models.TextField()             # 게시글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    updated_at = models.DateTimeField(auto_now=True)      # 수정 시간

    def __str__(self):
        return self.title
