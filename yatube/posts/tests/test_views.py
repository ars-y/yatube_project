from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase
from django import forms
from ..models import Post, Group


User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Test_slug',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес view-функций posts использует соответствующий шаблон."""
        templates_pages_name = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.pk}
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_name.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post_object = response.context['page_obj'][0]
        post_text_0 = post_object.text
        post_author_0 = post_object.author
        post_group_0 = post_object.group.title
        object_list = {
            post_text_0: PostPagesTests.post.text,
            post_author_0: PostPagesTests.post.author,
            post_group_0: PostPagesTests.group.title,
        }
        for value, expected in object_list.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        post_object = response.context['page_obj'][0]
        post_text_0 = post_object.text
        post_author_0 = post_object.author
        post_group_0 = post_object.group.title
        group_object = response.context['group']
        group_title = group_object.title
        group_slug = group_object.slug
        group_description = group_object.description
        object_list = {
            post_text_0: PostPagesTests.post.text,
            post_author_0: PostPagesTests.post.author,
            post_group_0: PostPagesTests.group.title,
            group_title: PostPagesTests.group.title,
            group_slug: PostPagesTests.group.slug,
            group_description: PostPagesTests.group.description,
        }
        for value, expected in object_list.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        post_object = response.context['page_obj'][0]
        post_text_0 = post_object.text
        post_author_0 = post_object.author
        post_group_0 = post_object.group.title
        object_list = {
            post_text_0: PostPagesTests.post.text,
            post_author_0: PostPagesTests.post.author,
            post_group_0: PostPagesTests.group.title,
            response.context['author'].username: (
                PostPagesTests.post.author.username
            ),
        }
        for value, expected in object_list.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        post_object = response.context['post']
        post_text = post_object.text
        post_author = post_object.author
        post_group = post_object.group.title
        object_list = {
            post_text: PostPagesTests.post.text,
            post_author: PostPagesTests.post.author,
            post_group: PostPagesTests.group.title,
        }
        for value, expected in object_list.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        post_object = response.context['post']
        post_text = post_object.text
        post_author = post_object.author
        post_group = post_object.group.title
        object_list = {
            post_text: PostPagesTests.post.text,
            post_author: PostPagesTests.post.author,
            post_group: PostPagesTests.group.title,
        }
        for value, expected in object_list.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)