from django.db import models
from django.template.defaultfilters import truncatechars


class Post(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['-created_at']

    def get_post_title(self):

        """
        Метод для отображения относящегося поста в админке
        """

        return f'Post: {self.post.title}'

    def get_short_text(self):
        """
         Метод для отображения текста комментария в админке до 20 символов.
        """
        return truncatechars(self.text, 20)




