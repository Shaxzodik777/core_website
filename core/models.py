from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse


# Create your models here.

# core_category
class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):  # отображение название объекта в списке элементов данной таблицы в админке
        return self.title

    # Category object(1)
    class Meta:
        # ordering = ['-title'] сортировка
        verbose_name = 'Категория'  # единственное число
        verbose_name_plural = 'Категории'  # множественное число


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', blank=True, null=True)
    image = models.ImageField(verbose_name='Фото', upload_to='articles/', blank=True, null=True)
    views = models.PositiveSmallIntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_id': self.pk})

    def img_preview(self):
        if not self.image:
            return ''
        return mark_safe(f'<img src="{self.image.url}" width="100" height="100">')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Comment
# author
# article
# created_at
# text


# admin
# 1, 2, 3
# Comment object (1)
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Отзыв')

    def __str__(self):
        return f'{self.author}: {self.article}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislikes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes',  null=True, blank=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='dislikes',  null=True, blank=True)



