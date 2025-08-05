from django import forms

from core.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']

    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 10}),
        help_text="Rate 1-10"
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )