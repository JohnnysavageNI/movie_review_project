from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Movie, Review, Comment
from .forms import ReviewForm

# Create your views here.


class MovieListView(ListView):
    model = Movie
    template_name = 'reviews/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 9


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'reviews/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.object)
        context['form'] = ReviewForm()
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
