from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Movie, Review, Comment

# Create your views here.


class MovieListView(ListView):
    model = Movie
    template_name = 'reviews/movie_list.html'
    context_object_name = 'movies'


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'reviews/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.object)
        return context
