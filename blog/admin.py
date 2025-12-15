from django.contrib import admin
from .models import Category, Tag, Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at', 'hit_count_display')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'content')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'image', 'author')
        }),
        ('Kategoriyalar va Teglar', {
            'fields': ('category', 'tags')
        }),
        ('Status va statistika', {
            'fields': ('is_published', 'is_featured', 'view_count')
        }),
    )
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)

    def hit_count_display(self, obj):
        return obj.hit_count.hits
    hit_count_display.short_description = 'Views'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text',)