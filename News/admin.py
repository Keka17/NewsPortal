

from django.contrib import admin
from .models import Post, Author, Category, PostCategory
from django.utils import timezone


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # можно добавить еще категории


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'news_type', 'publication_date', 'get_categories_str')
    # inlines = [PostCategoryInline]
    list_filter = ('author', 'publication_date', 'category')

    def get_categories_str(self, obj):
        return ", ".join([cat.category.category_name for cat in obj.postcategory_set.all()])


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)