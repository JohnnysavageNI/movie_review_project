from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))
APPROVAL = ((0, "Pending"), (1, "Approved"))

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=STATUS,
        default=1
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=STATUS,
        default=1
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Review by {self.user} for {self.movie}"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.IntegerField(
        choices=APPROVAL,
        default=0
    )

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment by {self.user} on {self.review}"
