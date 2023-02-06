import datetime

from django.test import TestCase

from post_app.models import Post, Comment
from post_app.serializers import PostSerializer


class PostSerializerTestCase(TestCase):
    def test_correct_serialization(self):
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post1 = Post.objects.create(title='TestTitle1', text='TestText1', created_at=dt)
        post2 = Post.objects.create(title='TestTitle2', text='TestText2', created_at=dt)
        post3 = Post.objects.create(title='TestTitle3', text='TestText3', created_at=dt)

        comment1 = Comment.objects.create(text='TestCommentText1', post=post1)
        comment2 =Comment.objects.create(text='TestCommentText2', post=post1)
        comment3 =Comment.objects.create(text='TestCommentText3', post=post3)

        data = PostSerializer([post1, post2, post3], many=True).data

        expected_data = [
            {
                'title': 'TestTitle1',
                'text': 'TestText1',
                'views_count': 0,
                'created_at': dt,
                'comments': [
                    {
                        'pk': comment2.id,
                        'text': 'TestCommentText2'
                    },
                    {
                        'pk': comment1.id,
                        'text': 'TestCommentText1'
                    }
                ]
            },
            {
                'title': 'TestTitle2',
                'text': 'TestText2',
                'views_count': 0,
                'created_at': dt,
                'comments': []
            },
            {
                'title': 'TestTitle3',
                'text': 'TestText3',
                'views_count': 0,
                'created_at': dt,
                'comments': [
                    {
                        'pk': comment3.id,
                        'text': 'TestCommentText3'
                    }
                ]
            }
        ]

        self.assertEqual(expected_data, data)
