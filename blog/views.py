from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.contenttypes.models import ContentType
from .models import Post, Category, Tag
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount, HitCountManager

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_published = Post.objects.filter(is_published=True)
        context['most_viewed'] = posts_published.order_by('-hit_count_generic__hits')[:5]

        # HitCount uses GenericForeignKey; filter by content type/object_pk instead of reverse relation
        post_ids = list(posts_published.values_list('pk', flat=True))
        post_content_type = ContentType.objects.get_for_model(Post)

        weekly_hits = sorted(
            HitCount.objects.filter(content_type=post_content_type, object_pk__in=post_ids),
            key=lambda hit: hit.hits_in_last(days=7),
            reverse=True,
        )[:5]
        weekly_popular_pks = [int(hit.object_pk) for hit in weekly_hits]
        context['weekly_popular'] = Post.objects.filter(pk__in=weekly_popular_pks)

        monthly_hits = sorted(
            HitCount.objects.filter(content_type=post_content_type, object_pk__in=post_ids),
            key=lambda hit: hit.hits_in_last(days=30),
            reverse=True,
        )[:5]
        monthly_popular_pks = [int(hit.object_pk) for hit in monthly_hits]
        context['monthly_popular'] = Post.objects.filter(pk__in=monthly_popular_pks)
        context['featured_posts'] = posts_published.filter(is_featured=True)[:3]
        context['categories'] = Category.objects.all()

        return context

class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    count_hit = True

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['comments'] = self.object.comments.select_related('author')
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