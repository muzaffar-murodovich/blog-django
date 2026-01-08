from django import forms
from django.utils.text import slugify
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Izohingizni shu yerga yozing..."}
            ),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Slug is generated automatically from the title
        fields = ["title", "content", "image", "category", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post sarlavhasi..."}),
            "content": forms.Textarea(
                attrs={"rows": 10, "placeholder": "Post matnini kiriting..."}
            ),
        }

    def save(self, commit=True):
        """
        Automatically generate a unique slug from the title
        when creating/updating a post.
        """
        instance = super().save(commit=False)

        if not instance.slug and instance.title:
            base_slug = slugify(instance.title)
            slug = base_slug
            counter = 1

            # Ensure slug is unique
            while Post.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            instance.slug = slug

        if commit:
            instance.save()
            self.save_m2m()

        return instance
