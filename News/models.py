from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
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
    category_name = models.CharField(max_length=30, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribed_categories')

    def __str__(self):
        return self.category_name

class Post(models.Model):

    article = 'AR'
    news = 'NE'

    TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_type = models.CharField(max_length=2, choices=TYPES, default=article)
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0)])

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