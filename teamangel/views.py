from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView


class PostList(ListView):
    model = Post
    ordering = '-pk' #ListView로 포스트 목록 페이지 만들기

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()  # post_list
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context  # -> post_list.html
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'teamangel/post_list.html',
        {
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
            'post_list': post_list,

        }
    )

class PostDetail(DetailView):
    model = Post


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload']
    template_name = 'teamangel/post_update_form.html'

def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().author:
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)
    else:
        raise PermissionDenied  # 포스트작성자마 수정할수있는 코드


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):  # form 기준
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # def form_valid(self, form):
    #     current_user = self.request.user
    #     if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
    #         form.instance.author = current_user