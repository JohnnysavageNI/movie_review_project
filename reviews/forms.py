from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'number',
            'max': 5,
            'min': 1,
            'class': 'form-control'
        })
    )

    class Meta:
        model = Review
        fields = ['rating']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Leave your comment...'
            }),
        }
