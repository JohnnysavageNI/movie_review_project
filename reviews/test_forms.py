from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Movie, Review, Comment

# Create your tests here.


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='pass1234'
        )

        self.movie = Movie.objects.create(
            title='Test Movie',
            genre='Drama',
            description='Test description'
        )
        self.review_url = reverse('movie_detail', args=[self.movie.pk])
        self.login_url = reverse('login')
        self.register_url = reverse('register')

    def test_registration_form(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_form(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, 302)

    def test_review_submission(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(self.review_url, {
            'rating': 4,
            'submit_review': True
        })
        self.assertRedirects(response, self.review_url)
        self.assertTrue(
            Review.objects.filter(
                user=self.user,
                movie=self.movie
            ).exists()
        )

    def test_duplicate_review_submission(self):
        Review.objects.create(user=self.user, movie=self.movie, rating=4)
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(self.review_url, {
            'rating': 5,
            'submit_review': True
        }, follow=True)
        self.assertContains(response, "already reviewed")

    def test_comment_requires_login(self):
        response = self.client.post(self.review_url, {
            'content': 'Nice!',
            'submit_comment': True
        })
        self.assertRedirects(
            response,
            f"{self.login_url}?next={self.review_url}"
        )

    def test_comment_submission(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(self.review_url, {
            'content': 'Test comment',
            'submit_comment': True
        })
        self.assertRedirects(response, self.review_url)
        self.assertTrue(
            Comment.objects.filter(
                user=self.user,
                movie=self.movie,
                content='Test comment'
            ).exists()
        )

    def test_comment_edit(self):
        comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            content="Old comment"
        )
        self.client.login(username='testuser', password='pass1234')
        edit_url = reverse('comment_edit', args=[self.movie.pk, comment.pk])
        response = self.client.post(edit_url, {'content': 'Edited comment'})
        self.assertRedirects(response, self.review_url)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Edited comment')
