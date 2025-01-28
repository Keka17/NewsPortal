
from django.core.cache import cache  # Correct import

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from django.utils.translation import gettext as _
from django.utils.translation import get_language


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def update_rating(self):
        author_posts = Post.objects.filter(author=self)
        author_comments = Comment.objects.filter(user=self.author)
        users_comments = Comment.objects.exclude(user=self.author)

        articles_rating = sum([post.rating * 3 for post
                               in author_posts.filter(news_type='AR')])

        comments_rating = sum([comment.rating for comment
                               in author_comments])

        user_rating = sum([comment.rating for comment
                             in users_comments])

        total = articles_rating + comments_rating + user_rating
        self.rating = total
        self.save(())

    # выводится имя атвора, а не его id
    def __str__(self):
        return self.author.username


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True, verbose_name=_('Категория'))
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_categories')

    category_name_en = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('Категория (английский)'))

    # нашла другой способ локализации моделей
    def get_localized_category(self):
        language = get_language()
        if language == 'en' and self.category_name_en:
            return self.category_name_en
        return self.category_name

    def __str__(self):
        return self.category_name

class Post(models.Model):

    article = 'AR'
    news = 'NE'

    TYPES = [
        (article, _('Статья')),
        (news, _('Новость'))
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Автор'))
    news_type = models.CharField(max_length=2, choices=TYPES, default=article, verbose_name=_('Тип публикации'))
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата'))
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name=_('Категория'))
    title = models.CharField(max_length=150, verbose_name=_('Заголовок'))
    text = models.TextField(verbose_name=_('Текст'))
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # поля для перевода на английский
    title_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Заголовок (английский)'))
    text_en = models.TextField(null=True, blank=True, verbose_name=_('Текст (английский)'))

    def __str__(self):
        return self.title

    # локализуем текст и заголовков на англ

    def get_localized_title(self):
        language = get_language()
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title

    def get_localized_text(self):
        language = get_language()
        if language == 'en' and self.text_en:
            return self.text_en
        return self.text


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()

    def preview(self):
        splitted_text = self.text.split()
        cropped_text = ' '.join(splitted_text[:124])
        return cropped_text + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()