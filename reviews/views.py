from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Avg, Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie, Review, Comment
from .forms import ReviewForm, CommentForm
from django.conf import settings


def movie_search(request):
    query = request.GET.get('q', '')
    results = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(genre__icontains=query) |
        Q(description__icontains=query)
    ).distinct()

    return render(request, 'reviews/movie_search.html', {
        'query': query,
        'results': results,
    })


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
        movie = self.object
        reviews = Review.objects.filter(movie=movie).select_related('user')
        context['reviews'] = reviews
        context['comments'] = Comment.objects.filter(movie=movie).select_related('user')
        context['review_form'] = ReviewForm()
        context['comment_form'] = CommentForm()
        context['average_rating'] = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        context['star_range'] = range(1, 6)
        return context

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        self.object = self.get_object()

        if "submit_review" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                if Review.objects.filter(movie=self.object, user=request.user).exists():
                    messages.error(request, "You have already reviewed this movie.")
                else:
                    Review.objects.create(
                        movie=self.object,
                        user=request.user,
                        rating=review_form.cleaned_data['rating']
                    )
                    messages.success(request, "Review submitted successfully!")
            else:
                messages.error(request, "Error submitting review.")
            return redirect('movie_detail', pk=self.object.pk)

        elif "submit_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.movie = self.object
                comment.save()
                messages.success(request, "Comment submitted successfully!")
            else:
                messages.error(request, "Error submitting comment.")
            return redirect('movie_detail', pk=self.object.pk)

        return self.get(request, *args, **kwargs)


@login_required
@require_POST
def delete_review(request, movie_id, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    messages.success(request, 'Review deleted!')
    return redirect('movie_detail', pk=movie_id)


@login_required
@require_POST
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    rating = request.POST.get('rating')
    if rating and rating.isdigit() and 1 <= int(rating) <= 5:
        review.rating = int(rating)
        review.save()
        messages.success(request, "Review updated!")
    else:
        messages.error(request, "Invalid rating value.")
    return redirect('movie_detail', pk=review.movie.pk)


@login_required
def comment_edit(request, pk, comment_id):
    movie = get_object_or_404(Movie, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() and comment.user == request.user:
            edited_comment = form.save(commit=False)
            edited_comment.save()
            messages.success(request, "Comment updated successfully!")
        else:
            messages.error(request, "Error updating comment.")
    return HttpResponseRedirect(reverse('movie_detail', args=[movie.pk]))


@login_required
def comment_delete(request, pk, comment_id):
    movie = get_object_or_404(Movie, pk=pk)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user == request.user:
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
    else:
        messages.error(request, "You are not allowed to delete this comment.")
    return redirect('movie_detail', pk=movie.pk)
