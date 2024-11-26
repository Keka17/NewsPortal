

from django.contrib import admin
from .models import Post, Author, Category, PostCategory #Make sure you import PostCategory


class PostCategoryInline(admin.TabularInline):  # Or StackedInline if you prefer
    model = PostCategory
    extra = 1  # Allow adding extra categories


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'news_type', 'publication_date', 'get_categories_str')
    inlines = [PostCategoryInline]

    def get_categories_str(self, obj):
        return ", ".join([cat.category.category_name for cat in obj.postcategory_set.all()]) # updated the queryset to use postcategory_set
    get_categories_str.short_description = 'Categories'


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)