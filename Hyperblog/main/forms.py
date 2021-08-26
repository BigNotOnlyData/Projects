from .models import Article, Comment
from django.forms import ModelForm, TextInput, Textarea


class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
        }),
            "body": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
        })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text"]
        widgets = {
            "comment_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите комментарий'
            })
        }