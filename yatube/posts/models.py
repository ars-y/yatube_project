from django.db import models
from django.contrib.auth import get_user_model
from yatube.settings import TRIM_STRING_LENGTH
from core.models import CreatedModel


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(
        verbose_name='URL',
        unique=True
    )
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(CreatedModel):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Введите имя автора',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        help_text='Группа, к которой относится пост',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text[:TRIM_STRING_LENGTH]

    class Meta:
        ordering = ['-created']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст нового комментария'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(CreatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Блогер',
        related_name='following'
    )

    class Meta:
        ordering = ['created']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_blogger_follower'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
