# -*- coding: utf-8 -*-
import re
import logging
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from watson import search as watson

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout as auth_logout, authenticate, login
from zavod.forms import QuestionForm, CustomUserCreationForm, CallbackForm
from zavod.constants import SPECIAL_FILTER_PARAMS
from zavod.models import Article, CategoryProduct, Product, News, Gallery, GalleryImage, Question, Employee, Tag
from zt.settings import EMAILS_FOR_CALLBACK


logger = logging.getLogger(__name__)


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
    out = {}
    ind_articles = enumerate(Article.objects.filter(published=True).order_by('-date_created').all()[0:3])
    ind_news = enumerate(News.objects.filter(published=True).order_by('-date_created').all()[0:2])
    out.update({'ind_articles': ind_articles})
    out.update({'ind_news': ind_news})
    return render(request, 'index.html', out)


def search(request):
    out = {}
    search_text = request.GET.get('search', '')
    search_results = watson.search(search_text)
    out.update({'menu_active_item': 'about'})
    out.update({'search_results': search_results})
    return render(request, 'zavod/search.html', out)


def contacts(request):
    out = {}
    out.update({'menu_active_item': 'contacts'})
    return render(request, 'contacts.html', out)


def prajjsy(request):
    out = {}
    price_lists = CategoryProduct.objects.filter(published=True).exclude(price_list='').values_list('price_list').distinct().all()
    out.update({'price_lists': price_lists})
    out.update({'menu_active_item': 'prajjsy'})
    return render(request, 'prajjsy.html', out)


def dostavka(request):
    out = {}
    out.update({'menu_active_item': 'dostavka'})
    return render(request, 'dostavka.html', out)


def mezhdunarodnaja_dostavka(request):
    out = {}
    out.update({'menu_active_item': 'dostavka'})
    return render(request, 'mezhdunarodnaja_dostavka.html', out)


def geografija_prodazh(request):
    out = {}
    out.update({'menu_active_item': 'dostavka'})
    return render(request, 'geografija_prodazh.html', out)


def dokumentatsija(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'dokumentatsija.html', out)


def razreshenie_na_primenenie(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'razreshenie_na_primenenie.html', out)


def sertifikaty(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'sertifikaty.html', out)


def tovarnye_znaki(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'tovarnye_znaki.html', out)


def mezhdunarodnye_tovarnye_znaki(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'mezhdunarodnye_tovarnye_znaki.html', out)


def tovarnyjj_znak_zachem_on(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'tovarnyjj_znak_zachem_on.html', out)


def tekhnicheskaja_dokumentatsija(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'tekhnicheskaja_dokumentatsija.html', out)


def zachem_nuzhna_dokumentatsija(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    return render(request, 'zachem_nuzhna_dokumentatsija.html', out)


def photogallery(request):
    out = {}
    events = Gallery.objects.filter(type='event', published=True).order_by('-date_created').all()
    products = Gallery.objects.filter(type='product', published=True).order_by('-date_created').all()
    gallery = Gallery.objects.filter(published=True).order_by('-date_created').all()
    out.update({'events': events})
    out.update({'products': products})
    out.update({'gallery': gallery})
    out.update({'menu_active_item': 'gallery'})
    return render(request, 'photogallery.html', out)


def photogallery_detail_page(request, page_number, photogallery_slug):
    out = {}
    gallery = get_object_or_404(Gallery, slug=photogallery_slug)
    start = (int(page_number) - 1) * 5 + 1
    gallery.gallery_images = GalleryImage.objects.filter(gallery=gallery).all()[start:start+5]
    out.update({'menu_active_item': 'gallery'})
    out.update({'gallery': gallery})
    return render(request, 'photogallery_detail.html', out)


def photogallery_detail(request, photogallery_slug):
    out = {}
    gallery = get_object_or_404(Gallery, slug=photogallery_slug)
    out.update({'menu_active_item': 'gallery'})
    out.update({'gallery': gallery})
    return render(request, 'photogallery_detail.html', out)


def about(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    if 'awards' in request.GET:
        return render(request, 'about_awards.html', out)
    elif 'partners' in request.GET:
        return render(request, 'about_partners.html', out)
    elif 'employee' in request.GET:
        return render(request, 'about_employee.html', out)
    elif 'review' in request.GET:
        return render(request, 'about_review.html', out)
    return render(request, 'about.html', out)


def nagrady(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    return render(request, 'about_awards.html', out)


def partnery(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    return render(request, 'about_partners.html', out)


def otzyvy(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    return render(request, 'about_review.html', out)


def employee(request):
    out = {}
    employees = Employee.objects.filter(published=True).all()
    i = 0
    all_employees = []
    set_by_five_employees = []
    for employee in employees:
        employee.is_first = False
        if i % 5 == 0:
            employee.is_first = True
        set_by_five_employees.append(employee)
        if len(set_by_five_employees) == 5:
            all_employees.append(set_by_five_employees)
            set_by_five_employees = []
        i += 1
    if set_by_five_employees:
        all_employees.append(set_by_five_employees)
    out.update({'employees': all_employees})
    out.update({'menu_active_item': 'about'})
    return render(request, 'about_employee.html', out)


def employee_info(request, employee_name):
    out = {}
    employee = Employee.objects.filter(published=True, name=employee_name).first()
    out.update({'employee': employee})
    out.update({'menu_active_item': 'about'})
    return render(request, 'about_employee_info.html', out)


def vacancy(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    return render(request, 'about_vacancy.html', out)


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
    questions = Question.objects.filter(published=True).all()
    out.update({'questions': questions})
    out.update({'menu_active_item': 'faq'})
    return render(request, 'about_faq.html', out)


def proizvodstvo_zavoda_triumf(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    return render(request, 'zavod/proizvodstvo_zavoda_triumf.html', out)


def gibkaja_sistema_skidok(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    return render(request, 'zavod/gibkaja_sistema_skidok.html', out)


def articles(request, page_number=1):
    out = {}
    article_objects = Article.objects.filter(published=True)
    tag = request.GET.get('tag', None)
    sort_type = request.GET.get('sort_type', 'date_created')
    ctype = ContentType.objects.get_for_model(Article.objects.model)
    if tag:
        article_objects = article_objects.filter(tags=Tag.objects.filter(title=tag).first())
    if sort_type == 'date_created':
        article_objects = article_objects.order_by('date_created')
    elif sort_type == 'popular':
        article_objects = article_objects.order_by('-views')
    elif sort_type == 'comment':
        article_objects = article_objects.extra(select={
            'comment_count' : """
                SELECT COUNT(*)
                FROM django_comments
                WHERE
                    django_comments.content_type_id={} AND
                    django_comments.object_pk=CAST({}.{} as CHAR)
            """.format ( ctype.pk,
                    article_objects.model._meta.db_table,
                    article_objects.model._meta.pk.name
                         ),
            },
            order_by=('-comment_count',)
        )
    elif sort_type == 'view':
        article_objects = article_objects.order_by('-views')
    start = (int(page_number) - 1) * 8
    ind_articles = enumerate(article_objects.all()[start:start+8])
    out.update({'ind_articles': ind_articles})
    out.update({'menu_active_item': 'articles'})
    out.update({'current_page_number': int(page_number)})
    all_page_count = article_objects.count() / 8 + 1
    if article_objects.count() % 8:
        all_page_count += 1
    out.update({'all_page_number': range(1, all_page_count)})
    return render(request, 'articles.html', out)


def articles_detail(request, article_slug):
    out = {}
    article = get_object_or_404(Article, slug=article_slug)
    article.views += 1
    article.save()
    related_article = Article.objects.filter(tags__in=article.tags.all()).exclude(pk=article.pk).order_by('-date_created').first()
    out.update({'article': article})
    print(related_article)
    print(article)
    out.update({'related_article': related_article})
    out.update({'menu_active_item': 'articles'})
    return render(request, 'articles_detail.html', out)


def articles_tag(request, tag):
    out = {}
    articles = Article.objects.filter(tags__title=tag, published=True)\
                      .order_by('-date_created').all()[:5]
    out.update({'menu_active_item': 'articles'})
    out.update({'articles': articles})
    return render(request, 'articles.html', out)


def articles_tag_page(request, page_number, tag):
    out = {}
    start = (int(page_number) - 1) * 5 + 1
    articles = Article.objects.filter(tags__title=tag, published=True)\
                      .order_by('-date_created').all()[start:start+5]
    out.update({'menu_active_item': 'articles'})
    out.update({'articles': articles})
    return render(request, 'articles.html', out)


def news_archive(request, page_number=1):
    out = {}
    news_objects = News.objects.filter(published=True)
    tag = request.GET.get('tag', None)
    sort_type = request.GET.get('sort_type', 'date_created')
    ctype = ContentType.objects.get_for_model(News.objects.model)
    if tag:
        news_objects = news_objects.filter(tags=Tag.objects.filter(title=tag).first())
    if sort_type == 'date_created':
        news_objects = news_objects.order_by('-date_created')
    elif sort_type == 'popular':
        news_objects = news_objects.order_by('-views')
    elif sort_type == 'comment':
        news_objects = news_objects.extra(select={
            'comment_count' : """
                SELECT COUNT(*)
                FROM django_comments
                WHERE
                    django_comments.content_type_id={} AND
                    django_comments.object_pk=CAST({}.{} as CHAR)
            """.format ( ctype.pk,
                    news_objects.model._meta.db_table,
                    news_objects.model._meta.pk.name
                         ),
            },
            order_by=('-comment_count',)
        )
    elif sort_type == 'view':
        news_objects = news_objects.order_by('-views')
    start = (int(page_number) - 1) * 6
    ind_news = enumerate(news_objects.all()[start:start+6])
    out.update({'ind_news': ind_news})
    out.update({'menu_active_item': 'news'})
    out.update({'current_page_number': int(page_number)})
    all_page_count = news_objects.count() / 6 + 1
    if news_objects.count() % 6:
        all_page_count += 1
    out.update({'all_page_number': range(1, all_page_count)})
    return render(request, 'news_archive.html', out)


def news(request):
    out = {}
    news = News.objects.filter(published=True).order_by('-date_created').all()[:5]
    out.update({'menu_active_item': 'news'})
    out.update({'news': news})
    return render(request, 'news.html', out)


def news_page(request, page_number):
    out = {}
    start = (int(page_number) - 1) * 5 + 1
    news = News.objects.filter(published=True).order_by('-date_created').all()[start:start+5]
    out.update({'menu_active_item': 'news'})
    out.update({'news': news})
    return render(request, 'news.html', out)


def news_detail(request, news_slug):
    out = {}
    news = get_object_or_404(News, slug=news_slug)
    news.views += 1
    news.save()
    related_news = News.objects.filter(tags__in=news.tags.all()).exclude(pk=news.pk).order_by('-date_created').all()[:7]
    out.update({'menu_active_item': 'news'})
    out.update({'news': news})
    out.update({'related_news': related_news})
    return render(request, 'news_detail.html', out)


def news_tag(request, tag):
    out = {}
    news = News.objects.filter(tags__title=tag, published=True)\
                   .order_by('-date_created').all()[:5]
    out.update({'menu_active_item': 'news'})
    out.update({'news': news})
    return render(request, 'news.html', out)


def news_tag_page(request, page_number, tag):
    out = {}
    start = (int(page_number) - 1) * 5 + 1
    news = News.objects.filter(tags__title=tag, published=True)\
                       .order_by('-date_created').all()[start:start+5]
    out.update({'menu_active_item': 'news'})
    out.update({'news': news})
    return render(request, 'news.html', out)


def get_product(request, slug, parent_category_slug=None, out={}):
    product = get_object_or_404(Product, slug=slug, category__slug=parent_category_slug)
    tab = request.GET.get('tab', 'description')
    template_name = 'product.html'
    if tab == 'description':
        template_name = 'product.html'
    elif tab == 'docs':
        template_name = 'product_docs.html'
    elif tab == 'photo':
        template_name = 'product_photo.html'
    elif tab == 'articles':
        template_name = 'product_articles.html'
        articles = set(product.category.articles.all()) | set(product.articles.all())
        product.ind_articles = enumerate(articles)
    elif tab == 'review':
        template_name = 'product_review.html'
    out.update({'product': product})
    out.update({'menu_active_item': 'catalog'})
    if request.method == 'POST':
        callback_form = CallbackForm(request.POST, request.FILES)
        if callback_form.is_valid():
            kwargs = dict(
                to=EMAILS_FOR_CALLBACK,
                from_email='from@example.com',
                subject=u'Заказ продукции',
                body=u'Поступил запрос на заказ продукции {} от {} (телефон для связи - {}, email - {}) с комментарием:\n\n"{}"'.format(
                    callback_form.cleaned_data['product'],
                    callback_form.cleaned_data['name'],
                    callback_form.cleaned_data['phone'],
                    callback_form.cleaned_data['email'],
                    callback_form.cleaned_data['comment'],
                ),
            )
            message = EmailMessage(**kwargs)
            for attachment in request.FILES.getlist('file_field'):
                message.attach(attachment.name, attachment.read(), attachment.content_type)
            message.send()
            logger.info(u'Send callback with text: {}'.format(kwargs['body']))
    callback_form = CallbackForm()
    out.update({'callback_form': callback_form})
    return render(request, template_name, out)


def catalog(request):
    out = {}
    category_products = CategoryProduct.objects.filter(published=True, parent_id=None).all()
    for category_product in category_products:
        category_product.number = Product.objects.filter(published=True, category=category_product).count()
        for child_category in CategoryProduct.objects.filter(published=True, parent_id=category_product.id).all():
            category_product.number += Product.objects.filter(published=True, category=child_category).count()
    ind_category_products = enumerate(category_products)
    out.update({'ind_category_products': ind_category_products})
    out.update({'menu_active_item': 'catalog'})
    out.update({'category_products': category_products})
    if request.GET.get('expand', 'true') == 'true':
        return render(request, 'catalog_expand.html', out)
    return render(request, 'catalog.html', out)


def catalog_category(request, category_slug, parent_category_slug=None):
    out = {}
    category = CategoryProduct.objects.filter(slug=category_slug).first()
    out.update({'menu_active_item': 'catalog'})
    if category:
        category.number = Product.objects.filter(published=True, category=category).count()
        for child_category in CategoryProduct.objects.filter(published=True, parent_id=category.id).all():
            category.number += Product.objects.filter(published=True, category=child_category).count()
        if CategoryProduct.objects.filter(parent_id=category.id):
            title = 'Вложенные категории'
            subcategories = CategoryProduct.objects.filter(parent_id=category.id, published=True).all()
            for subcategory in subcategories:
                subcategory.number = Product.objects.filter(published=True, category=subcategory).count()
                for child_category in CategoryProduct.objects.filter(published=True, parent_id=subcategory.id).all():
                    subcategory.number += Product.objects.filter(published=True, category=child_category).count()
            template_name = 'catalog_category.html'
            ind_subcategory = enumerate(subcategories)
            if request.GET.get('expand', 'true') == 'true':
                template_name = 'catalog_category_expand.html'
            out.update({'subcategories': subcategories, 'title': title, 'category': category, 'request': request,
                        'ind_subcategory': ind_subcategory})
            return render(request, template_name, out)
        else:
            title = 'Список продуктов'
            products = Product.objects.all().filter(category=category, published=True)
            template_name = 'catalog_category_products.html'
            ind_products = enumerate(products)
            if request.GET.get('expand', 'true') == 'true':
                template_name = 'catalog_category_products_expand.html'
            out.update({'products': products, 'parent': category, 'title': title, 'category': category,
                        'request': request, 'ind_products': ind_products})
            return render(request, template_name, out)
    else:
        return get_product(request, category_slug, parent_category_slug, out)


def product_or_products(request, slug, parent_category_slug=None, category_slug=None):
    out = {}
    out.update({'menu_active_item': 'catalog'})
    product = Product.objects.filter(slug=slug).first()
    if product:
        return get_product(request, slug, category_slug, out)
    title = 'Список продуктов во вложенной категории'
    category = get_object_or_404(CategoryProduct, slug=slug)
    products = Product.objects.filter(category=category, published=True).all()
    out.update({'products': products, 'title': title, 'category': category})
    return render(request, 'catalog_category.html', out)


def products_search(request):
    search_param = {}
    out = {}
    out.update({'menu_active_item': 'catalog'})
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
    out.update({'search_results': result})
    return render(request, 'zavod/search.html', out)


# def email_question(request):
    # if request.method == 'POST':
    #     form = CallbackForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         kwargs = dict(
    #             to=EMAIL_FOR_CALLBACK,
    #             from_email='from@example.com',
    #             subject=u'Заказ продукции',
    #             body=u'Поступил запрос на заказ продукции {} от {} (телефон для связи - {}, email - {}) с комментарием:\n\n"{}"'.format(
    #                 form.cleaned_data['product'],
    #                 form.cleaned_data['name'],
    #                 form.cleaned_data['phone'],
    #                 form.cleaned_data['email'],
    #                 form.cleaned_data['comment'],
    #             ),
    #         )
    #         message = EmailMessage(**kwargs)
    #         for attachment in request.FILES:
    #             message.attach(attachment.name, attachment.read(), attachment.content_type)
    #             message.attach_file(attachment.path)
    #         message.send()
    #         logger.info(u'Send callback with text: {}'.format(
    #             u'Поступил запрос на заказ продукции {} от {} (телефон для связи - {}, email - {}) с комментарием:\n\n"{}"'.format(
    #                 form.cleaned_data['product'],
    #                 form.cleaned_data['name'],
    #                 form.cleaned_data['phone'],
    #                 form.cleaned_data['email'],
    #                 form.cleaned_data['comment'],
    #             )
    #         ))
    # else:
    #     form = CallbackForm()
