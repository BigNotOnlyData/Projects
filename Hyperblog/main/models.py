from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField("Заголовок статьи", max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author')
    body = models.TextField("Текст статьи")
    pub_date = models.DateTimeField("Дата публиуации")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('main:detail', args=[str(self.id)])
        return reverse('main:person')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentator')
    comment_text = models.CharField("Текст комментария", max_length=300)
    comment_date = models.DateTimeField("Дата комментария")

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
