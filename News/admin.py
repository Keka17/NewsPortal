

from django.contrib import admin
from .models import Post, Author, Category, PostCategory 


class PostCategoryInline(admin.TabularInline):  
    model = PostCategory
    extra = 1  


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'news_type', 'publication_date', 'get_categories_str')
    inlines = [PostCategoryInline]

    def get_categories_str(self, obj):
        return ", ".join([cat.category.category_name for cat in obj.postcategory_set.all()]) 
    get_categories_str.short_description = 'Categories'


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
