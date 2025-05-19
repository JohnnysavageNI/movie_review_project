from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Movie, Review, Comment
from .forms import ReviewForm
from django.db.models import Avg

# Create your views here.


class MovieListView(ListView):
    model = Movie
    template_name = 'reviews/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 9


@method_decorator(login_required, name='dispatch')
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'reviews/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.object
        reviews = Review.objects.filter(movie=movie)

        context['reviews'] = reviews
        context['form'] = ReviewForm()
        context['average_rating'] = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = self.object
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=self.object.pk)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
