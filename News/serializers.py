from rest_framework import serializers
from .models import Post, Category

class PostSerializer(serializers.ModelSerializer):

    # Для читабельного отображеня автора и категории/й
    author_name = serializers.CharField(source='author.author.username', read_only=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'news_type', 'publication_date', 'categories', 'title', 'text', 'rating']

    # Вывод названия категорий
    def get_categories(self, obj):
        return [category.category_name for category in obj.category.all()]
