from django import forms
from django.core.exceptions import ValidationError
from blog_app.models import Blog, Post


class BlogForm(forms.Form):
    name = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea)

    name.widget.attrs.update({'class': 'form-control'})
    description.widget.attrs.update({'class': 'form-control'})

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Blog.objects.filter(name=name).count():
            raise ValidationError(f'Blog name "{name}" already exists')
        return name

    def save(self):
        Blog.objects.create(**self.cleaned_data, author=self.author)


class PostForm(forms.Form):
    title = forms.CharField(max_length=80)
    content = forms.CharField(widget=forms.Textarea)

    title.widget.attrs.update({'class': 'form-control'})
    content.widget.attrs.update({'class': 'form-control'})

    def __init__(self, blog, *args, **kwargs):
        self.blog = blog
        super().__init__(*args, **kwargs)

    def save(self):
        Post.objects.create(**self.cleaned_data, blog=self.blog)
