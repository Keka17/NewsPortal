from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-publication_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.count()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'search_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if len(context['posts']) == 1:
            return redirect('post_detail', pk=context['posts'][0].pk)
        else:
            return self.render_to_response(context)


class NewsCreate(CreateView, PermissionRequiredMixin):
    permission_required = ('News.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creating_view'] = 'news_create'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'NE'
        post.save()
        return redirect(post.get_absolute_url())

class NewsEdit(UpdateView, PermissionRequiredMixin):
    permission_required = ('News.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_queryset(self):
        return super().get_queryset().filter(news_type='NE')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return redirect(post.get_absolute_url())


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list') 
    def get_queryset(self):
        return super().get_queryset().filter(news_type='NE')

class ArticlesCreate(CreateView, PermissionRequiredMixin):
    permission_required = ('News.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creating_view'] = 'articles_create'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'AR'
        post.save()
        return redirect(post.get_absolute_url())


class ArticlesEdit(UpdateView, LoginRequiredMixin, TemplateView, PermissionRequiredMixin):
    permission_required = ('News.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_success_url(self):
        return reverse('articles_edit', args=[self.object.pk])

    def get_queryset(self):
        return super().get_queryset().filter(news_type='AR')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return redirect(post.get_absolute_url())



class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_queryset(self):
        return super().get_queryset().filter(news_type='AR')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


