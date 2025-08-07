from django import forms

from users.models import UserProfile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar_url', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    # Optional: Add username editing (requires User model)
    username = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username