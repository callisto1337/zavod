# -*- coding: utf-8 -*-
from itertools import chain
import re
import logging
import collections
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.db.models import Q
from watson import search as watson

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, authenticate, login
from zavod.forms import QuestionForm, CustomUserCreationForm, CallbackForm, SubscriptionForm, CallMeForm
from zavod.constants import SPECIAL_FILTER_PARAMS, SUBSCRIPTION_TYPE
from zavod.models import Article, CategoryProduct, Product, News, Gallery, GalleryImage, Question, Employee, Tag, \
    ProductProperty, Property, Department, Subscription
from zt.settings import EMAILS_FOR_CALLBACK


logger = logging.getLogger(__name__)


def registration(request, next_url='main'):
    if request.method == 'POST':
        form_reg = CustomUserCreationForm(request.POST)
        if form_reg.is_valid():
            form_reg.save()
            user = authenticate(
                username=form_reg.cleaned_data['email'],
                password=form_reg.cleaned_data['password1']
            )
            if user is not None:
                login(request, user)
        messages.add_message(request, messages.INFO, form_reg.errors)
    return redirect(next_url)


def log_in(request, next_url='main'):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            messages.add_message(request, messages.INFO, u'Неправильная пара email-пароль')
    return redirect(next_url)


def logout(request):
    auth_logout(request)
    return redirect('/')


def main(request):
    out = {}
    ind_articles = enumerate(Article.objects.filter(published=True).order_by('-date_created').all()[0:3])
    ind_news = enumerate(News.objects.filter(published=True).order_by('-date_created').all()[0:2])
    black_friday_product = Product.objects.filter(is_black_friday=True).first()
    gallery = black_friday_product.category.galleries.filter(published=True).first()
    if not gallery and black_friday_product.category.parent_id:
        gallery = black_friday_product.category.parent_id.galleries.filter(published=True).first()
    out.update({'gallery': gallery})
    out.update({'ind_articles': ind_articles})
    out.update({'ind_news': ind_news})
    out.update({'black_friday_product': black_friday_product})
    out.update({'title': u'Завод Триумф'})
    return render(request, 'index.html', out)


def search(request):
    out = {}
    search_text = request.GET.get('search', '')
    search_results = watson.search(search_text)
    search_results_count = search_results.count()
    page_number = request.GET.get('page', 1)
    start = (int(page_number) - 1) * 10
    out.update({'current_page_number': int(page_number)})
    all_page_count = search_results.count() / 10 + 1
    if search_results.count() % 10:
        all_page_count += 1
    search_results = search_results[start:start+10]
    out.update({'all_page_number': range(1, all_page_count)})
    out.update({'menu_active_item': 'search'})
    out.update({'search_results': search_results})
    out.update({'search_results_count': search_results_count})
    out.update({'search_text': search_text})
    out.update({'title': u'Поиск'})
    return render(request, 'search.html', out)


def contacts(request):
    out = {}
    employees_by_departments = []
    departments = Department.objects.all()
    for department in departments:
        chunks = [department.employees.all()[x:x+2] for x in xrange(0, len(department.employees.all()), 2)]
        employees_by_departments += chunks
    out.update({'employees_by_departments': employees_by_departments})
    out.update({'menu_active_item': 'contacts'})
    if request.method == 'POST':
        callback_form = CallbackForm(request.POST)
        if callback_form.is_valid():
            kwargs = dict(
                to=EMAILS_FOR_CALLBACK,
                from_email='from@example.com',
                subject=u'Письмо с сайта zavod',
                body=u'Через форму обратной связи было отправлено сообщение. Автор: {} (телефон для связи - {}, email - {}).\nСообщение:\n\n"{}"'.format(
                    callback_form.cleaned_data['name'],
                    callback_form.cleaned_data['phone'],
                    callback_form.cleaned_data['email'],
                    callback_form.cleaned_data['comment'],
                ),
            )
            message = EmailMessage(**kwargs)
            message.send()
            logger.info(u'Send callback with text: {}'.format(kwargs['body']))
    callback_form = CallbackForm()
    out.update({'callback_form': callback_form})
    location = request.GET.get('location', 'office')
    out.update({'title': u'Контакты'})
    if location == 'manufacture':
        return render(request, 'contacts_manufacture.html', out)
    else:
        return render(request, 'contacts.html', out)


def prajjsy(request):
    out = {}
    price_lists = CategoryProduct.objects.filter(published=True).exclude(price_list='').values_list('price_list').distinct().all()
    out.update({'price_lists': price_lists})
    out.update({'vodovodjanye_podogrevateli': CategoryProduct.objects.filter(slug='vodovodjanye-podogrevateli').first()})
    out.update({'parovodjanye_podogrevateli': CategoryProduct.objects.filter(slug='parovodjanye-podogrevateli').first()})
    out.update({'podogrevateli_parovye': CategoryProduct.objects.filter(slug='podogrevateli-parovye-emkostnye-tipa-vpe-std').first()})
    out.update({'serija_ts_565': CategoryProduct.objects.filter(slug='serija-ts-565').first()})
    out.update({'serija_ts_566': CategoryProduct.objects.filter(slug='serija-ts-566').first()})
    out.update({'serija_ts_567': CategoryProduct.objects.filter(slug='serija-ts-567').first()})
    out.update({'grjazeviki_teplovykh_punktov': CategoryProduct.objects.filter(slug='grjazeviki-dlja-teplovykh-punktov-gtp-serija-ts-569').first()})
    out.update({'vozdukhosborniki_a1i': CategoryProduct.objects.filter(slug='vozdukhosborniki-a1i').first()})
    out.update({'elevatory': CategoryProduct.objects.filter(slug='elevatory').first()})
    out.update({'menu_active_item': 'prajjsy'})
    out.update({'title': u'Прайс-листы'})
    return render(request, 'prajjsy.html', out)


def dostavka(request):
    out = {}
    out.update({'menu_active_item': 'dostavka'})
    out.update({'title': u'Доставка'})
    return render(request, 'dostavka.html', out)


def mezhdunarodnaja_dostavka(request):
    out = {}
    out.update({'menu_active_item': 'dostavka'})
    out.update({'title': u'Международная доставка'})
    return render(request, 'mezhdunarodnaja_dostavka.html', out)


def geografija_prodazh(request):
    out = {}
    out.update({'menu_active_item': 'dostavka'})
    out.update({'title': u'География продаж'})
    return render(request, 'geografija_prodazh.html', out)


def dokumentatsija(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Документация'})
    return render(request, 'dokumentatsija.html', out)


def razreshenie_na_primenenie(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Разрешение на применение'})
    return render(request, 'razreshenie_na_primenenie.html', out)


def sertifikaty(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Сертификаты'})
    return render(request, 'sertifikaty.html', out)


def tovarnye_znaki(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Товарные знаки'})
    return render(request, 'tovarnye_znaki.html', out)


def mezhdunarodnye_tovarnye_znaki(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Международные товарные знаки'})
    return render(request, 'mezhdunarodnye_tovarnye_znaki.html', out)


def tovarnyjj_znak_zachem_on(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Контакты'})
    return render(request, 'tovarnyjj_znak_zachem_on.html', out)


def tekhnicheskaja_dokumentatsija(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Техническая документация'})
    return render(request, 'tekhnicheskaja_dokumentatsija.html', out)


def zachem_nuzhna_dokumentatsija(request):
    out = {}
    out.update({'menu_active_item': 'dokumentatsija'})
    out.update({'title': u'Контакты'})
    return render(request, 'zachem_nuzhna_dokumentatsija.html', out)


def photogallery(request, page_number=1):
    out = {}
    start = (int(page_number) - 1) * 5
    gallery = Gallery.objects.filter(published=True, galleryvideo=None).order_by('-date_created').all()
    out.update({'current_page_number': int(page_number)})
    all_page_count = gallery.count() / 6 + 1
    if gallery.count() % 6:
        all_page_count += 1
    gallery = gallery[start:start+5]
    out.update({'all_page_number': range(1, all_page_count)})
    out.update({'gallery': gallery})
    out.update({'menu_active_item': 'gallery'})
    out.update({'title': u'Фотогалерея'})
    return render(request, 'photogallery.html', out)


def photogallery_detail_page(request, photogallery_slug, page_number=1):
    out = {}
    gallery = get_object_or_404(Gallery, slug=photogallery_slug)
    gallery.gallery_images = GalleryImage.objects.filter(gallery=gallery).all()
    out.update({'menu_active_item': 'gallery'})
    out.update({'gallery': gallery})
    out.update({'title': gallery.title})
    return render(request, 'photogallery_detail.html', out)


def videogallery(request, page_number=1):
    out = {}
    start = (int(page_number) - 1) * 5
    gallery = Gallery.objects.filter(published=True, is_otzyv=False).exclude(galleryvideo=None).order_by('-date_created').all()
    out.update({'current_page_number': int(page_number)})
    all_page_count = gallery.count() / 6 + 1
    if gallery.count() % 6:
        all_page_count += 1
    gallery = gallery[start:start+5]
    out.update({'all_page_number': range(1, all_page_count)})
    out.update({'gallery': gallery})
    out.update({'menu_active_item': 'gallery'})
    out.update({'title': u'Видеогалерея'})
    return render(request, 'videogallery.html', out)


def videootzyvy(request, page_number=1):
    out = {}
    start = (int(page_number) - 1) * 5
    gallery = Gallery.objects.filter(published=True, is_otzyv=True).exclude(galleryvideo=None).order_by('-date_created').all()
    out.update({'current_page_number': int(page_number)})
    all_page_count = gallery.count() / 6 + 1
    if gallery.count() % 6:
        all_page_count += 1
    gallery = gallery[start:start+5]
    out.update({'all_page_number': range(1, all_page_count)})
    out.update({'gallery': gallery})
    out.update({'menu_active_item': 'gallery'})
    out.update({'title': u'Видеоотзывы'})
    return render(request, 'videootzyvy.html', out)


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
    out.update({'title': u'О компании'})
    return render(request, 'about.html', out)


def nagrady(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    out.update({'title': u'Награды компании'})
    return render(request, 'about_awards.html', out)


def partnery(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    out.update({'title': u'Партнеры компании'})
    return render(request, 'about_partners.html', out)


def otzyvy(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    out.update({'title': u'Отзывы о компании'})
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
    out.update({'title': u'Сотрудники компании'})
    return render(request, 'about_employee.html', out)


def employee_info(request, employee_name):
    out = {}
    employee = Employee.objects.filter(published=True, name=employee_name).first()
    out.update({'employee': employee})
    out.update({'menu_active_item': 'about'})
    out.update({'title': employee.first_name + ' ' + employee.last_name})
    return render(request, 'about_employee_info.html', out)


def vacancy(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    out.update({'title': u'Вакансии'})
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
    out.update({'title': u'Часто задаваемые вопросы'})
    return render(request, 'about_faq.html', out)


def proizvodstvo_zavoda_triumf(request):
    out = {}
    out.update({'menu_active_item': 'about'})
    out.update({'title': u'Контакты'})
    return render(request, 'zavod/proizvodstvo_zavoda_triumf.html', out)


def gibkaja_sistema_skidok(request):
    out = {}
    out.update({'menu_active_item': 'prajjsy'})
    out.update({'title': u'Гибкая система скидок'})
    return render(request, 'gibkaja_sistema_skidok.html', out)


def articles(request, page_number=1, tag_in_url=None):
    out = {}
    out.update({'url_for_pages': 'articles_page'})
    article_objects = Article.objects.filter(published=True)
    tag = request.GET.get('tag', None)
    sort_type = request.GET.get('sort_type', 'date_created')
    ctype = ContentType.objects.get_for_model(Article.objects.model)
    if tag:
        article_objects = article_objects.filter(tags=Tag.objects.filter(title=tag).first())
    if tag_in_url:
        out.update({'url_for_pages': 'articles_tag_page'})
        out.update({'tag_in_url': tag_in_url})
        article_objects = article_objects.filter(tags=Tag.objects.filter(title=tag_in_url).first())
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
    start = (int(page_number) - 1) * 9
    if start == 0:
        ind_articles = enumerate(article_objects.all()[start:start+8])
    else:
        ind_articles = enumerate(article_objects.all()[start-1:start+8])
    out.update({'ind_articles': ind_articles})
    out.update({'menu_active_item': 'articles'})
    out.update({'current_page_number': int(page_number)})
    all_page_count = (article_objects.count() + 1) / 9 + 1
    if (article_objects.count() + 1) % 9:
        all_page_count += 1
    out.update({'all_page_number': range(1, all_page_count)})
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            Subscription.objects.create(
                email=subscription_form.cleaned_data['email'],
                type=SUBSCRIPTION_TYPE[u'Статьи']
            )
    subscription_form = SubscriptionForm()
    out.update({'subscription_form': subscription_form})
    out.update({'title': u'Статьи'})
    return render(request, 'articles.html', out)


def articles_detail(request, article_slug):
    out = {}
    article = get_object_or_404(Article, slug=article_slug)
    article.views += 1
    article.save()
    related_article = Article.objects.filter(tags__in=article.tags.all()).exclude(pk=article.pk).order_by('-date_created').first()
    out.update({'article': article})
    out.update({'related_article': related_article})
    out.update({'menu_active_item': 'articles'})
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            Subscription.objects.create(
                email=subscription_form.cleaned_data['email'],
                type=SUBSCRIPTION_TYPE[u'Статьи']
            )
    subscription_form = SubscriptionForm()
    out.update({'subscription_form': subscription_form})
    out.update({'title': article.title})
    return render(request, 'articles_detail.html', out)


def news_archive(request, page_number=1, tag_in_url=None):
    out = {}
    out.update({'url_for_pages': 'news_archive_page'})
    news_objects = News.objects.filter(published=True)
    tag = request.GET.get('tag', None)
    sort_type = request.GET.get('sort_type', 'date_created')
    ctype = ContentType.objects.get_for_model(News.objects.model)
    if tag:
        news_objects = news_objects.filter(tags=Tag.objects.filter(title=tag).first())
    if tag_in_url:
        out.update({'url_for_pages': 'news_tag_page'})
        out.update({'tag_in_url': tag_in_url})
        news_objects = news_objects.filter(tags=Tag.objects.filter(title=tag_in_url).first())
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
    out.update({'title': u'Архив новостей'})
    return render(request, 'news_archive.html', out)


def news(request):
    out = {}
    news = News.objects.filter(published=True).order_by('-date_created').all()
    articles = Article.objects.filter(published=True).order_by('-date_created').all()
    out.update({'menu_active_item': 'news'})
    out.update({'slider_news': news[:3]})
    out.update({'medium_news': news[3:5]})
    out.update({'one_line_news': news[5:9]})
    out.update({'image_articles': articles[0:2]})
    out.update({'not_image_articles': articles[2]})
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            Subscription.objects.create(
                email=subscription_form.cleaned_data['email'],
                type=SUBSCRIPTION_TYPE[u'Новости']
            )
    subscription_form = SubscriptionForm()
    out.update({'subscription_form': subscription_form})
    out.update({'title': u'Новости'})
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
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            Subscription.objects.create(
                email=subscription_form.cleaned_data['email'],
                type=SUBSCRIPTION_TYPE[u'Новости']
            )
    subscription_form = SubscriptionForm()
    out.update({'subscription_form': subscription_form})
    out.update({'title': news.title})
    return render(request, 'news_detail.html', out)


def get_product(request, path, out={}):
    slug = path.split('/')[-2]
    if len(path.split('/')) > 2:
        category_slug = path.split('/')[-3]
    if category_slug:
        product = get_object_or_404(Product, slug=slug, category__slug=category_slug)
    else:
        product = get_object_or_404(Product, slug=slug)
    tab = request.GET.get('tab', 'description')
    template_name = 'product.html'
    if tab == 'description':
        template_name = 'product.html'
    elif tab == 'docs':
        template_name = 'product_docs.html'
    elif tab == 'photo':
        galleries = product.category.galleries.filter(published=True).all()
        if product.category.parent_id:
            galleries = chain(galleries, product.category.parent_id.galleries.filter(published=True).all())
        galleries = set(galleries)
        out.update({'galleries': galleries})
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
                body=u'Поступил запрос на заказ продукции {} в количестве {} штук от {} (телефон для связи - {}, email - {}) с комментарием:\n\n"{}"'.format(
                    callback_form.cleaned_data['product'],
                    callback_form.cleaned_data['count'],
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
    out.update({'title': product.name})
    return render(request, template_name, out)


def catalog(request):
    out = {}
    category_products = CategoryProduct.objects.filter(published=True, parent_id=None).all()
    for category_product in category_products:
        category_products_all = Product.objects.filter(published=True, category=category_product)
        category_product.number = category_products_all.count()
        for child_category in CategoryProduct.objects.filter(published=True, parent_id=category_product.id).all():
            category_product.number += Product.objects.filter(published=True, category=child_category).count()
    ind_category_products = enumerate(category_products)
    out.update({'ind_category_products': ind_category_products})
    out.update({'menu_active_item': 'catalog'})
    out.update({'category_products': category_products})
    out.update({'title': u'Каталог'})
    if request.GET.get('expand', 'true') == 'true':
        return render(request, 'catalog_expand.html', out)
    return render(request, 'catalog.html', out)


def catalog_category(request, category_path):
    out = {}
    category_slug = category_path.split('/')[-2]
    if len(category_path.split('/')) > 2:
        parent_category_slug = category_path.split('/')[-3]
    category = CategoryProduct.objects.filter(slug=category_slug).first()
    out.update({'menu_active_item': 'catalog'})
    out.update({'category_path': category_path})
    if category:
        category.number = Product.objects.filter(published=True, category=category).count()
        for child_category in CategoryProduct.objects.filter(published=True, parent_id=category.id).all():
            category.number += Product.objects.filter(published=True, category=child_category).count()
        if CategoryProduct.objects.filter(parent_id=category.id):
            title = 'Вложенные категории'
            subcategories = CategoryProduct.objects.filter(parent_id=category.id, published=True).all()
            for subcategory in subcategories:
                subcategory_products_all = Product.objects.filter(published=True, category=subcategory)
                subcategory.number = subcategory_products_all.count()
                for child_category in CategoryProduct.objects.filter(published=True, parent_id=subcategory.id).all():
                    subcategory_products_all = subcategory_products_all | Product.objects.filter(published=True, category=child_category)
                    subcategory.number += Product.objects.filter(published=True, category=child_category).count()
                subcategory.min_price = None
                for product in subcategory_products_all:
                    current = product.properties.filter(Q(property__title__contains='Цена')).first()
                    try:
                        if current and not subcategory.min_price:
                            subcategory.min_price = float(unicode(current.value).replace(u' ', u'').replace(u'\xa0', u''))
                        if current and float(current.value.replace(' ', '').replace(u'\xa0', '')) < subcategory.min_price:
                            subcategory.min_price = float(current.value.replace(' ', '').replace(u'\xa0', ''))
                    except Exception:
                        pass
            template_name = 'catalog_category.html'
            ind_subcategory = enumerate(subcategories)
            if request.GET.get('expand', 'true') == 'true':
                template_name = 'catalog_category_expand.html'
            out.update({'subcategories': subcategories, 'title': title, 'category': category, 'request': request,
                        'ind_subcategory': ind_subcategory})
            out.update({'title': category.name})
            return render(request, template_name, out)
        else:
            title = 'Список продуктов'
            products = Product.objects.filter(category=category, published=True)
            for product in products.all():
                product.properties_dict = product.properties.values('property__title', 'value')
            template_name = 'catalog_category_products.html'
            ind_products = enumerate(products.all())
            properties = []
            properties_ids = ProductProperty.objects.filter(product__in=products).values_list('property', flat=True).distinct().all()
            for property_id in properties_ids:
                properties.append(Property.objects.get(pk=property_id))
            properties.sort()
            # найти минимальное и максимальное значение в каждом свойстве
            for property in properties:
                all_value = list(ProductProperty.objects.filter(product__in=products, property=property).
                                 values_list('value', flat=True))
                all_value_int = []
                for value in all_value:
                    try:
                        all_value_int.append(float(value.replace(',', '.').replace(' ', '').replace(u'\xa0', '').replace(u'\u2014', '').replace('-', '')))
                    except Exception:
                        all_value_int = [0]
                property.min = unicode(min(all_value_int)).replace(',', '.')
                property.max = unicode(max(all_value_int)).replace(',', '.')
                property.get_min = property.min
                property.get_max = property.max
            # фильтрация по гет-параметрам
            for property in properties:
                property_get_param_from = property.slug + '_from'
                property_value_from = request.GET.get(property_get_param_from, None)
                if property_value_from:
                    property.get_min = property_value_from
                    for product in products:
                        if not float(product.properties.filter(property=property).first().value.replace(',', '.')) >= float(property_value_from):
                            products = products.exclude(pk=product.pk)
                property_get_param_to = property.slug + '_to'
                property_value_to = request.GET.get(property_get_param_to, None)
                if property_value_to:
                    property.get_max = property_value_to
                    for product in products:
                        if not float(product.properties.filter(property=property).first().value.replace(',', '.')) <= float(property_value_to):
                            products = products.exclude(pk=product.pk)
            # отфильтровали
            products = products.all()
            for product in products:
                product.properties_dict = {}
                for property in properties:
                    prop = ProductProperty.objects.filter(product=product, property=property).first()
                    if prop:
                        product.properties_dict.update(
                            {
                                property.title + ', ' + property.units: prop.value
                            }
                        )
                    else:
                        product.properties_dict.update(
                            {
                                property.title + ', ' + property.units: ' - '
                            }
                        )
                product.properties_dict = collections.OrderedDict(sorted(product.properties_dict.items()))
            new_properties = []
            for property in properties:
                new_properties.append(u'{}, {}'.format(property.title, property.units))
            new_properties.sort()
            if request.GET.get('expand', 'true') == 'true':
                template_name = 'catalog_category_products_expand.html'
            out.update({'products': products, 'parent': category, 'title': title, 'category': category,
                        'request': request, 'ind_products': ind_products, 'properties': new_properties,
                        'properties_objs': properties})
            if request.method == 'POST':
                callback_form = CallbackForm(request.POST, request.FILES)
                if callback_form.is_valid():
                    kwargs = dict(
                        to=EMAILS_FOR_CALLBACK,
                        from_email='from@example.com',
                        subject=u'Заказ продукции',
                        body=u'Поступил запрос на заказ продукции {} в количестве {} штук от {} (телефон для связи - {}, email - {}) с комментарием:\n\n"{}"'.format(
                            callback_form.cleaned_data['product'],
                            callback_form.cleaned_data['count'],
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
            out.update({'title': category.name})
            return render(request, template_name, out)
    else:
        return get_product(request, category_path, out)


def product_or_products(request, path):
    out = {}
    slug = path.split('/')[-2]
    if len(path.split('/')) > 2:
        category_slug = path.split('/')[-3]
    out.update({'menu_active_item': 'catalog'})
    product = Product.objects.filter(slug=slug).first()
    if product:
        return get_product(request, path, out)
    title = 'Список продуктов во вложенной категории'
    category = get_object_or_404(CategoryProduct, slug=slug)
    products = Product.objects.filter(category=category, published=True).all()
    out.update({'products': products, 'title': title, 'category': category})
    out.update({'title': category.name})
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
    out.update({'title': u'Поиск'})
    return render(request, 'zavod/search.html', out)


def callme_form_process(request, next_url='main'):
    if request.method == 'POST':
        callme_form = CallMeForm(request.POST)
        if callme_form.is_valid():
            kwargs = dict(
                to=EMAILS_FOR_CALLBACK,
                from_email='from@example.com',
                subject=u'Просьба перезвонить',
                body=u'Поступил просьба перезвонить: {}, телефон для связи - {}, с {} до {}.'.format(
                    callme_form.cleaned_data['name'],
                    callme_form.cleaned_data['phone'],
                    callme_form.cleaned_data['time_from'],
                    callme_form.cleaned_data['time_to'],
                ),
            )
            message = EmailMessage(**kwargs)
            message.send()
            logger.info(u'Send callme with text: {}'.format(kwargs['body']))
    return redirect(next_url)


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
