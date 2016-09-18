# -*- coding: utf-8 -*-
import re
from django.contrib.auth.forms import AuthenticationForm
from watson import search as watson

from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as auth_logout, authenticate, login
from zavod.forms import QuestionForm, CustomUserCreationForm
from zavod.constants import SPECIAL_FILTER_PARAMS
from zavod.models import Article, CategoryProduct, Product, News, Gallery, GalleryImage


def registration(request):
    out = {}
    if request.method == 'POST':
        form_reg = CustomUserCreationForm(request.POST)
        if form_reg.is_valid():
            form_reg.save()
            return redirect('/')
    else:
        form_reg = CustomUserCreationForm()
    out.update({'form_reg': form_reg})
    return render(request, 'zavod/login.html', out)


def log_in(request):
    if not request.user.is_authenticated:
        out = {}
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                out.update({"error": 1})
        else:
            form = AuthenticationForm()
        out.update({'form_auth': form})
        return render(request, 'zavod/login.html', out)
    else:
        return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')


def main(request):
    return render(request, 'index.html')


def search(request):
    search_text = request.GET.get('text', '')
    search_results = watson.search(search_text)
    return render(request, 'zavod/search.html', {'search_results': search_results})


def contacts(request):
    return render(request, 'zavod/contacts.html')


def prajjsy(request):
    return render(request, 'zavod/prajjsy.html')


def dostavka(request):
    return render(request, 'zavod/dostavka.html')


def mezhdunarodnaja_dostavka(request):
    return render(request, 'zavod/mezhdunarodnaja_dostavka.html')


def geografija_prodazh(request):
    return render(request, 'zavod/geografija_prodazh.html')


def dokumentatsija(request):
    return render(request, 'dokumentatsija.html')


def razreshenie_na_primenenie(request):
    return render(request, 'razreshenie_na_primenenie.html')


def sertifikaty(request):
    return render(request, 'sertifikaty.html')


def tovarnye_znaki(request):
    return render(request, 'tovarnye_znaki.html')


def mezhdunarodnye_tovarnye_znaki(request):
    return render(request, 'zavod/mezhdunarodnye_tovarnye_znaki.html')


def tovarnyjj_znak_zachem_on(request):
    return render(request, 'zavod/tovarnyjj_znak_zachem_on.html')


def tekhnicheskaja_dokumentatsija(request):
    return render(request, 'tekhnicheskaja_dokumentatsija.html')


def zachem_nuzhna_dokumentatsija(request):
    return render(request, 'zavod/zachem_nuzhna_dokumentatsija.html')


def photogallery(request):
    out = {}
    events = Gallery.objects.filter(type='event', published=True).order_by('date_created').all()
    products = Gallery.objects.filter(type='product', published=True).order_by('date_created').all()
    out.update({'events': events})
    out.update({'products': products})
    return render(request, 'zavod/photogallery.html', out)


def photogallery_detail_page(request, page_number, photogallery_slug):
    gallery = get_object_or_404(Gallery, slug=photogallery_slug)
    start = (int(page_number) - 1) * 5 + 1
    gallery.gallery_images = GalleryImage.objects.filter(gallery=gallery).all()[start:start+5]
    return render(request, 'zavod/photogallery_detail.html', {'gallery': gallery})


def photogallery_detail(request, photogallery_slug):
    gallery = get_object_or_404(Gallery, slug=photogallery_slug)
    return render(request, 'zavod/photogallery_detail.html', {'gallery': gallery})


def news(request):
    return render(request, 'zavod/news.html')


def about(request):
    if 'awards' in request.GET:
        return render(request, 'about_awards.html')
    elif 'partners' in request.GET:
        return render(request, 'about_partners.html')
    elif 'employee' in request.GET:
        return render(request, 'about_employee.html')
    elif 'review' in request.GET:
        return render(request, 'about_review.html')
    return render(request, 'about.html')


def nagrady(request):
    return render(request, 'about_awards.html')


def partnery(request):
    return render(request, 'about_partners.html')


def otzyvy(request):
    return render(request, 'about_review.html')


def employee(request):
    return render(request, 'about_employee.html')


def employee_info(request, employee_name):
    if employee_name:
        return render(request, 'about_employee_info.html')
    return render(request, 'about_employee_info.html')


def vacancy(request):
    return render(request, 'about_vacancy.html')


def faq(request):
    out = {}
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save()
            out.update({'question_asked': True})
        else:
            out.update({'error': 'Что-то пошло не так!'})
    question_form = QuestionForm()
    out.update({'question_form': question_form})
    return render(request, 'zavod/about_faq.html', out)


def proizvodstvo_zavoda_triumf(request):
    return render(request, 'zavod/proizvodstvo_zavoda_triumf.html')


def gibkaja_sistema_skidok(request):
    return render(request, 'zavod/gibkaja_sistema_skidok.html')


def articles(request):
    articles = Article.objects.filter(published=True).order_by('date_created').all()[:5]
    return render(request, 'articles.html', {'articles': articles})


def articles_page(request, page_number):
    start = (int(page_number) - 1) * 5 + 1
    articles = Article.objects.filter(published=True).order_by('date_created').all()[start:start+5]
    return render(request, 'articles.html', {'articles': articles})


def articles_detail(request, article_slug):
    article = get_object_or_404(Article, slug=article_slug)
    article.views += 1
    article.save()
    return render(request, 'articles_detail.html', {'article': article})


def articles_tag(request, tag):
    articles = Article.objects.filter(tags__title=tag, published=True)\
                      .order_by('date_created').all()[:5]
    return render(request, 'articles.html', {'articles': articles})


def articles_tag_page(request, page_number, tag):
    start = (int(page_number) - 1) * 5 + 1
    articles = Article.objects.filter(tags__title=tag, published=True)\
                      .order_by('date_created').all()[start:start+5]
    return render(request, 'articles.html', {'articles': articles})


def news_archive(request):
    news = News.objects.filter(published=True).order_by('date_created').all()[:5]
    return render(request, 'news_archive.html', {'news': news})


def news(request):
    news = News.objects.filter(published=True).order_by('date_created').all()[:5]
    return render(request, 'news.html', {'news': news})


def news_page(request, page_number):
    start = (int(page_number) - 1) * 5 + 1
    news = News.objects.filter(published=True).order_by('date_created').all()[start:start+5]
    return render(request, 'news.html', {'news': news})


def news_detail(request, news_slug):
    news = get_object_or_404(News, slug=news_slug)
    return render(request, 'news_detail.html', {'news': news})


def news_tag(request, tag):
    news = News.objects.filter(tags__title=tag, published=True)\
                   .order_by('date_created').all()[:5]
    return render(request, 'news.html', {'news': news})


def news_tag_page(request, page_number, tag):
    start = (int(page_number) - 1) * 5 + 1
    news = News.objects.filter(tags__title=tag, published=True)\
                       .order_by('date_created').all()[start:start+5]
    return render(request, 'news.html', {'news': news})


def get_product(request, slug):
    out = {}
    product = get_object_or_404(Product, slug=slug)
    tab = request.GET.get('tab', 'description')
    template_name = 'product.html'
    print tab
    if tab == 'description':
        template_name = 'product.html'
    elif tab == 'docs':
        template_name = 'product_docs.html'
    elif tab == 'photo':
        template_name = 'product_photo.html'
    elif tab == 'articles':
        template_name = 'product_articles.html'
    elif tab == 'review':
        template_name = 'product_review.html'
    out.update({'product': product})
    return render(request, template_name, {'product': product})


def catalog(request):
    category_products = CategoryProduct.objects.filter(published=True).annotate(number=Count('product')).all()
    if 'expand' in request.GET:
        return render(request, 'catalog_expand.html', {'category_products': category_products})
    return render(request, 'catalog.html', {'category_products': category_products})


def catalog_category(request, category_slug, parent_category_slug=None):
    category = CategoryProduct.objects.filter(slug=category_slug).first()
    if category:
        if CategoryProduct.objects.filter(parent_id=category.id):
            title = 'Вложенные категории'
            subcategories = CategoryProduct.objects.filter(parent_id=category.id, published=True).all()
            template_name = 'catalog_category.html'
            if 'expand' in request.GET:
                template_name = 'catalog_category_expand.html'
            return render(request, template_name, {'subcategories': subcategories, 'title': title,
                                                   'category': category, 'request': request})
        else:
            title = 'Список продуктов'
            products = Product.objects.all().filter(category=category, published=True)
            template_name = 'catalog_category.html'
            if 'expand' in request.GET:
                template_name = 'catalog_category_expand.html'
            return render(request, template_name, {'products': products, 'parent': category, 'title': title,
                                                   'category': category, 'request': request})
    else:
        out = {}
        product = get_object_or_404(Product, slug=category_slug)
        tab = request.GET.get('tab', 'description')
        template_name = 'product.html'
        if tab == 'description':
            template_name = 'product.html'
        elif tab == 'docs':
            template_name = 'product_docs.html'
            product.documents = product.category.files.all()
        elif tab == 'photo':
            template_name = 'product_photo.html'
            product.photos = product.images.all()
        elif tab == 'articles':
            template_name = 'product_articles.html'
            product.articles = Article.objects.all()
        elif tab == 'review':
            template_name = 'product_review.html'
        product.string_properties = []
        for key, value in product.properties.items():
            product.string_properties.append(u'{}: {}'.format(key, value))
        out.update({'product': product})
        return render(request, template_name, {'product': product})


def product_or_products(request, slug, parent_category_slug=None, category_slug=None):
    out = {}
    product = Product.objects.filter(slug=slug).first()
    if product:
        get_product(request, category_slug)
    title = 'Список продуктов во вложенной категории'
    category = get_object_or_404(CategoryProduct, slug=slug)
    products = Product.objects.filter(category=category, published=True).all()
    out.update({'products': products, 'title': title, 'category': category})
    return render(request, 'catalog_category.html', out)


def products_search(request):
    search_param = {}
    result = Product.objects
    for param in request.GET:
        if param in SPECIAL_FILTER_PARAMS:
            result = result.filter(properties__has_key=unicode(param[:-4]))
            for product in result:
                param_value_str = (product.properties.get(unicode(param[:-4]), None))
                param_value = float(re.findall(SPECIAL_FILTER_PARAMS.get(param), param_value_str)[0])
                if param[-3:] == 'max' and param_value > float(request.GET.get(param, None)):
                    result = result.exclude(pk=product.pk)
                elif param[-3:] == 'min' and param_value < float(request.GET.get(param, None)):
                    result = result.exclude(pk=product.pk)
        else:
            search_param.update({
                u'properties__{}'.format(param): request.GET.get(param, None),
            })
            result = result.filter(**search_param)
    return render(request, 'zavod/search.html', {'search_results': result})
