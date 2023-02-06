from django.contrib import admin

from .models import Comment, Post


class CommentInline(admin.TabularInline):
    """
    StackedInline для добавления(изменение) комментариев на странице
    создания(изменения) поста.
    """

    model = Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_post_title', 'get_short_text', 'created_at']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    inlines = [CommentInline]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
