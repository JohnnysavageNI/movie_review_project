from django.urls import path
from . import views
from .views import MovieListView, MovieDetailView, edit_review, delete_review

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('search/', views.movie_search, name='movie_search'),
    path("<int:pk>/edit_comment/<int:comment_id>/", views.comment_edit, name="comment_edit"),
    path("<int:pk>/delete_comment/<int:comment_id>/", views.comment_delete, name="comment_delete"),
]
