from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Movie, Review, Comment

# Create your tests here.


class ViewTests(TestCase):
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
        self.detail_url = reverse('movie_detail', args=[self.movie.pk])
        self.list_url = reverse('movie_list')

    def test_movie_list_view_status_code(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_movie_list_template_used(self):
        response = self.client.get(self.list_url)
        self.assertTemplateUsed(response, 'reviews/movie_list.html')

    def test_movie_detail_view_status_code(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_invalid_movie(self):
        response = self.client.get(reverse('movie_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_review_submission_authenticated(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(self.detail_url, {
            'rating': 5,
            'submit_review': True
        })
        self.assertRedirects(response, self.detail_url)
        self.assertTrue(
            Review.objects.filter(
                movie=self.movie,
                user=self.user
            ).exists()
        )

    def test_duplicate_review_submission(self):
        Review.objects.create(movie=self.movie, user=self.user, rating=4)
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(self.detail_url, {
            'rating': 5,
            'submit_review': True
        }, follow=True)

        self.assertContains(response, "already reviewed")

    def test_comment_submission_authenticated(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(self.detail_url, {
            'content': 'Test comment',
            'submit_comment': True
        })
        self.assertRedirects(response, self.detail_url)
        self.assertTrue(
            Comment.objects.filter(
                movie=self.movie,
                user=self.user
            ).exists()
        )

    def test_comment_submission_unauthenticated(self):
        response = self.client.post(self.detail_url, {
            'content': 'Should not post',
            'submit_comment': True
        })
        login_url = reverse('login')
        self.assertRedirects(response, f"{login_url}?next={self.detail_url}")

    def test_edit_comment_view_only_by_owner(self):
        comment = Comment.objects.create(
            movie=self.movie,
            user=self.user,
            content="Old comment"
        )
        edit_url = reverse('comment_edit', args=[self.movie.pk, comment.pk])
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(edit_url, {'content': 'Updated comment'})
        self.assertRedirects(response, self.detail_url)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment')

    def test_delete_comment_view_only_by_owner(self):
        comment = Comment.objects.create(
            movie=self.movie,
            user=self.user,
            content="Delete me"
        )
        delete_url = reverse(
            'comment_delete',
            args=[self.movie.pk, comment.pk]
        )
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(delete_url)
        self.assertRedirects(response, self.detail_url)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
