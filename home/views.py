from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.core.paginator import Paginator


def post_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query), Q(content__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)

    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'home/post_list.html', context=context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'home/post_detail.html', {'post': post})


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        user = UserRegisterForm(request.POST)
        if user.is_valid():
            user.save()
            username = user.cleaned_data.get('username')
            messages.success(request, f'Account create for {username}')
            login(request, authenticate(
                username=user.cleaned_data['username'],
                password=user.cleaned_data['password1']
            ))
            return redirect('index')
    else:
        user = UserRegisterForm()
    return render(request, 'home/register.html', {'user_form': user})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/post/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.save()
        return redirect('/post/')
