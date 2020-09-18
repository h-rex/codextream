from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from course.models import Category
from blog.models import Post, CategoryBlog, Comment, SubCommnet


# Create your views here


def blogHome(request):
    cat_menu = Category.objects.all().order_by('name')
    allPosts = Post.objects.all()
    category = CategoryBlog.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(allPosts, 9)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    parms = {
        'category': category,
        'posts': posts,
        'cat_menu': cat_menu,
    }
    return render(request, 'blog/blogHome.html', parms)


def blogPost(request, slug):
    allPosts = Post.objects.all()
    cat_menu = Category.objects.all().order_by('name')

    try:
        post = Post.objects.get(slug=slug)
    except:
        raise Http404("Post Does Not Exist")
    post.views += 1
    post.save()

    if request.method == 'POST':
        comm = request.POST.get('comm')
        comm_id = request.POST.get('comm_id')

        if comm_id:
            SubCommnet(post=post,
                       user=request.user,
                       comm=comm,
                       comment=Comment.objects.get(id=int(comm_id))).save()
        else:
            Comment(post=post,
                    user=request.user,
                    comm=comm).save()
    comments = []

    for c in Comment.objects.filter(post=post):
        comments.append([c, SubCommnet.objects.filter(comment=c)])
    context = {
        'comments': comments,
        'allPosts': allPosts,
        'post': post,
        'cat_menu': cat_menu,
        'pop_post': Post.objects.order_by('-views'),
    }
    return render(request, 'blog/blogPost.html', context)


def list_of_post_by_category(request, slug):
    categories = CategoryBlog.objects.all()
    cat_menu = Category.objects.all().order_by('name')
    if slug:
        category = get_object_or_404(CategoryBlog, slug=slug)
        post = Post.objects.filter(category=category)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 9)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'categories': categories, 'category': category, 'post': posts, 'cat_menu': cat_menu, }
    return render(request, 'blog/blog_categories.html', context)


def blogSearch(request):
    cat_menu = Category.objects.all().order_by('name')
    categories = CategoryBlog.objects.all()
    context = {}
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # q = request.GET.get('q')
    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(body_text__icontains=query)
    ).distinct()

    if posts.count() == 0:
        messages.warning(request, "No search result found please refine your query")

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 9)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    parms = {
        'post': post,
        'cat_menu': cat_menu,
        'categories': categories,
        'title': f'{query}',
    }
    return render(request, 'blog/blogSearch.html', parms)
