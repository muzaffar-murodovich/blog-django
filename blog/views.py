from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from hitcount.views import HitCountDetailView


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_viewed'] = Post.objects.filter(is_published=True).order_by('-hit_count_generic__hits')[:5]
        context['featured_posts'] = Post.objects.filter(is_published=True, is_featured=True)[:3]
        context['weekly_popular'] = context['most_viewed']
        context['categories'] = Category.objects.all()

        return context


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    count_hit = True

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'], is_published=True)
        post.save()

        self.object = post
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=category, is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = get_object_or_404(Category, slug=self.kwargs['slug']).name
        return context


class TagPostListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(tags__in=[tag], is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = get_object_or_404(Tag, slug=self.kwargs['slug']).name
        return context
