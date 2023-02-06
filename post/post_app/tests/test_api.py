import datetime

from django.db.models import Prefetch, Subquery, OuterRef
from django.urls import reverse
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase

from post_app.models import Post, Comment
from post_app.serializers import PostSerializer


class PostsApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.post1 = Post.objects.create(title='TestTitle1', text='TestText1', created_at=self.dt)
        self.post2 = Post.objects.create(title='TestTitle2', text='TestText2', created_at=self.dt)
        self.post3 = Post.objects.create(title='TestTitle3', text='TestText3', created_at=self.dt)

        self.comment1 = Comment.objects.create(text='TestCommentText1', post=self.post1)
        self.comment2 = Comment.objects.create(text='TestCommentText2', post=self.post1)
        self.comment3 = Comment.objects.create(text='TestCommentText3', post=self.post3)

    def test_get_list(self):
        url = reverse('post-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))

        expected_data = [
            {
                'title': 'TestTitle1',
                'text': 'TestText1',
                'views_count': 0,
                'created_at': self.dt,
                'comments': [
                    {
                        'pk': self.comment2.id,
                        'text': 'TestCommentText2'
                    },
                ]
            },
            {
                'title': 'TestTitle2',
                'text': 'TestText2',
                'views_count': 0,
                'created_at': self.dt,
                'comments': []
            },
            {
                'title': 'TestTitle3',
                'text': 'TestText3',
                'views_count': 0,
                'created_at': self.dt,
                'comments': [
                    {
                        'pk': self.comment3.id,
                        'text': 'TestCommentText3'
                    }
                ]
            }
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_get_detail(self):
        self.assertEqual(0, self.post1.views_count)
        self.post1.views_count += 1

        url = reverse('post-detail', args=(self.post1.id,))
        response = self.client.get(url)

        data = PostSerializer(self.post1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, self.post1.views_count)
        self.assertEqual(data, response.data)







