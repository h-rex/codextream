import time

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
# Create your views here.

#
# def index(request):
#     msg = "Welcome to my website"
#     return HttpResponse(msg)
from django.views.generic import TemplateView, DetailView, ListView
from course.models import Course, Category, Contact


def home(request):
    post = Course.objects.all()
    cat_menu = Category.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(post, 8)

    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Course.objects.filter(
        upload_time__gte=week_ago).order_by('-views')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    parms = {
        'cat_menu': cat_menu,
        'post': posts,
        'pop_post': Course.objects.order_by('-views'),
        'trends': trends[:5],
        'paginator': paginator,
        # 'posts': posts,
    }
    return render(request, 'course/home.html', parms)


def coursePost(request, id, slug):
    cat_menu = Category.objects.all().order_by('name')
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Course.objects.filter(
        upload_time__gte=week_ago).order_by('-views')
    try:
        course = Course.objects.get(pk=id, slug=slug)
    except:
        raise Http404("Post Does Not Exist")

    course.views += 1
    course.save()

    parms = {
        'cat_menu': cat_menu,
        'course': course,
        'trends': trends[:5],
    }
    return render(request, 'course/course_post.html', parms)


def search(request):
    cat_menu = Category.objects.all().order_by('name')
    context = {}
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # q = request.GET.get('q')
    post = Course.objects.filter(
        Q(title__icontains=query) |
        Q(body_text__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct()

    page = request.GET.get('page', 1)
    paginator = Paginator(post, 8)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    parms = {
        'cat_menu': cat_menu,
        'posts': posts,
        'title': f'{query}',
        'post_count': f'{post.count()}',
    }
    return render(request, 'course/search_post.html', parms)


def category(request, query):
    cat_menu = Category.objects.all().order_by('name')
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    accept = ['trending', 'popular']

    q = query.lower()
    if q in accept:
        if q == accept[0]:
            post = Course.objects.filter(
                upload_time__gte=week_ago).order_by('-views')
            page = request.GET.get('page', 1)
            paginator = Paginator(post, 8)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            parms = {
                'cat_menu': cat_menu,
                'posts': posts,
                'title': 'Trending Courses',
                'pop_post': Course.objects.order_by('-views')[:9],
            }
        elif q == accept[1]:
            post = Course.objects.order_by('-views')
            page = request.GET.get('page', 1)
            paginator = Paginator(post, 8)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            parms = {
                'cat_menu': cat_menu,
                'posts': posts,
                'title': 'Popular Courses',
                'pop_post': Course.objects.order_by('-views')[:9],
            }
        else:
            messages.error(request, 'Not Found')

    return render(request, 'course/all.html', parms)


class CourseCategory(ListView):
    model = Category
    cat_menus = Category.objects.all().order_by('name')
    template_name = 'course/course_category.html'
    paginate_by = 8

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        cat_menu = Course.objects.filter(category=self.category)
        return cat_menu

    def get_context_data(self, **kwargs):
        return context


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, 'Please fill the form correctly.')
        else:
            messages.success(request, 'Your message has been successfully sent.')
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
    return render(request, 'course/contact.html', {'cat_menu': cat_menu})


def donate(request):
    parms = {
        'cat_menu' : cat_menu
    }
    return render(request,'course/donate.html',parms)

def privacy(request):
    cat_menu = Category.objects.all().order_by('name')
    parms = {
        'cat_menu' : cat_menu
    }
    return render(request,'course/privacy_policy.html',parms)

def team(request):
    cat_menu = Category.objects.all().order_by('name')
    parms = {
        'cat_menu' : cat_menu
    }
    return render(request,'course/team.html',parms)
