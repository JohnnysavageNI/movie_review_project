from django.contrib import admin
from .models import Movie, Review, Comment

# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'created_on')
