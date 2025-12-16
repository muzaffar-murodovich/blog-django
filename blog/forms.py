from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Izohingizni shu yerga yozing...'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post sarlavhasi...'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Post matnini kiriting...'}),
        }