from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from course.models import Category
from freepdf.models import Pdf, CategoryPdf


def home(request):
    pdf = Pdf.objects.all()
    cat_menu = Category.objects.all().order_by('name')
    category = CategoryPdf.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(pdf, 10)

    try:
        pdfs = paginator.page(page)
    except PageNotAnInteger:
        pdfs = paginator.page(1)
    except EmptyPage:
        pdfs = paginator.page(paginator.num_pages)

    parms = {'cat_menu': cat_menu,
             'pdfs': pdfs,
             'category': category,
             'paginator': paginator, }
    return render(request, 'freepdf/home.html', parms)


def pdfPost(request, slug):
    pdf = Pdf.objects.all()
    cat_menu = Category.objects.all().order_by('name')
    category = CategoryPdf.objects.all()

    try:
        pdfs = Pdf.objects.get(slug=slug)
    except:
        raise Http404("Post Does Not Exist")

    parms = {
        'cat_menu': cat_menu,
        'pdf': pdf,
        'pdfs': pdfs,
        'category': category,
    }
    return render(request, 'freepdf/freePdf_post.html', parms)


def pdfCategory(request, slug):
    category = CategoryPdf.objects.all()
    cat_menu = Category.objects.all().order_by('name')

    if slug:
        categories = get_object_or_404(CategoryPdf, slug=slug)
        pdf = Pdf.objects.filter(category_pdf=categories)

    page = request.GET.get('page', 1)
    paginator = Paginator(pdf, 10)

    try:
        pdfs = paginator.page(page)
    except PageNotAnInteger:
        pdfs = paginator.page(1)
    except EmptyPage:
        pdfs = paginator.page(paginator.num_pages)
    parms = {
        'cat_menu': cat_menu,
        'category': category,
        'categories': categories,
        'pdfs': pdfs,
    }
    return render(request, 'freepdf/freePdf_category.html', parms)


def pdfSearch(request):
    cat_menu = Category.objects.all().order_by('name')
    categories = CategoryPdf.objects.all()
    context = {}
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    # q = request.GET.get('q')
    pdfs = Pdf.objects.filter(
        Q(title__icontains=query) |
        Q(category_pdf__name__icontains=query)
    ).distinct()
    if pdfs.count() == 0:
        messages.warning(request, "No search result found please refine your query")
        
    page = request.GET.get('page', 1)
    paginator = Paginator(pdfs, 10)

    try:
        pdf = paginator.page(page)
    except PageNotAnInteger:
        pdf = paginator.page(1)
    except EmptyPage:
        pdf = paginator.page(paginator.num_pages)
    parms = {
        'pdf': pdf,
        'cat_menu': cat_menu,
        'categories': categories,
        'title': f'{query}',
    }
    return render(request, 'freepdf/freePdf_search.html', parms)
