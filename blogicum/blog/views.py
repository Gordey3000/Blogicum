import datetime as dt

from blog.models import Category, Comment, Post
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, UserForm

User = get_user_model()


def get_page_context(posts):
    return Paginator(posts, 10)


def queryset_post():
    return Post.objects.all().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.datetime.now())


def index(request):
    posts = queryset_post().order_by('-pub_date').annotate(
        comment_count=Count('comment')
    )
    paginator = get_page_context(posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, 'blog/index.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=profile
    ).order_by('-pub_date').annotate(
        comment_count=Count('comment')
    )
    paginator = get_page_context(posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile,
               'page_obj': page_obj,
               }
    return render(request, 'blog/profile.html', context)


def edit_profile(request):
    instance = get_object_or_404(User, username=request.user)
    form = UserForm(request.POST, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('blog:profile', username=request.user)
    return render(request, 'blog/create.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related(
        'category', 'location', 'author'), id=post_id)
    if post.author != request.user:
        post = get_object_or_404(Post.objects.select_related(
            'category', 'location', 'author').filter(
            pub_date__lt=dt.datetime.now(),
            category__is_published=True,
            is_published=True,
            id=post_id
        ))
    form = CommentForm()
    comments = Comment.objects.all().filter(post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=instance)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id, comment_id=None):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if comment_id:
            form = CommentForm(
                instance=Comment.objects.get(id=comment_id),
                data=request.POST
            )
        else:
            form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = Comment.objects.get(pk=comment_id)
    if request.user != user.author:
        return redirect('blog:post_detail', post_id)
    form = CommentForm(
        request.POST or None,
        files=request.FILES or None,
        instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    context = {
        'form': form,
        'comment': comment,
        'is_edit': True}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, id=comment_id)
    if request.user != instance.author:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html')


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True,
                                slug=category_slug)
    )
    posts = Post.objects.select_related('category').filter(
        is_published=True, category=category,
        pub_date__lt=dt.datetime.now()
    ).order_by('-pub_date')
    paginator = get_page_context(posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)
