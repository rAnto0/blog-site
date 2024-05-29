from django import forms
from .models import Category, ArticleAdditionalDescription


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    additional_info = forms.ModelChoiceField(queryset=ArticleAdditionalDescription.objects.all(), required=False)
