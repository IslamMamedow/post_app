from django.db.models import Prefetch, Subquery, OuterRef
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from post_app.models import Post, Comment
from post_app.serializers import PostSerializer


class ListPostView(mixins.ListModelMixin,
                   GenericViewSet):
    """
    API-endpoint для получения списка постов с одним последним комментарием
    """
    queryset = Post.objects.all().prefetch_related(
        Prefetch(
            'comments',
            queryset=Comment.objects.filter(
                id__in=Subquery(
                    Comment.objects.filter(post_id=OuterRef('post_id')).values_list('id', flat=True)[:1]
                )
            )
        )
    )

    serializer_class = PostSerializer


class DetailPostView(mixins.RetrieveModelMixin,
                     GenericViewSet):
    """
    API-endpoint для получения отдельного поста
    """
    queryset = Post.objects.all().prefetch_related('comments')
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        При получении поста увеличивает счетчик просмотров
        """
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



