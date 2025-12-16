from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from hitcount.models import HitCount
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from hitcount.views import HitCountDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm


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


class PostDetailView(HitCountDetailView, FormMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    count_hit = True
    form_class = CommentForm

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if not request.user.is_authenticated:
            return render(request, self.template_name, self.get_context_data(form=form, error="Izoh qoldirish uchun tizimga kirishingiz kerak."))

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

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

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_published = False 
        return super().form_valid(form)