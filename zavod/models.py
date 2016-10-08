# -*- coding: utf-8 -*-
import json
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import User, UserManager, AbstractBaseUser
from django.contrib.postgres.fields import JSONField

from zt.settings import EMAILS_FOR_FAQ


class JSONFieldCustom(JSONField):
    def value_from_object(self, obj):
        return json.dumps(super(JSONFieldCustom, self).value_from_object(obj))


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class News(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default='', unique=True)
    preview_post = models.TextField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='news', default=None, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name='news', default=None, null=True, blank=True)
    author = models.TextField(max_length=200, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class File(models.Model):
    title = models.CharField(max_length=100)
    file_content = models.FileField(upload_to='media/files/', blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class CategoryProduct(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, default='', unique=True)
    parent_id = models.ForeignKey("CategoryProduct", default=None, null=True, blank=True)
    title = models.CharField(max_length=100, default='')
    text = models.TextField(default='')
    images = models.ManyToManyField(Image, related_name='categories', default=None, null=True, blank=True)
    files = models.ManyToManyField(File, related_name='categories', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='')
    category = models.ForeignKey(CategoryProduct)
    product_text = models.TextField()
    title = models.CharField(max_length=200, default='')
    seo_title = models.CharField(max_length=300, default='')
    seo_description = models.CharField(max_length=300, default='')
    seo_keywords = models.CharField(max_length=300, default='')
    properties = JSONFieldCustom(default='')
    images = models.ManyToManyField(Image, related_name='products', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('get_product', args=[self.slug])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Article(models.Model):
    published = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, default='', unique=True)
    preview_post = models.TextField(max_length=200)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    author = models.TextField(max_length=200, default='')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='articles', default=None, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name='articles', default=None, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='articles', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Gallery(models.Model):
    published = models.BooleanField(default=True)
    type = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='', unique=True)
    text = models.TextField()
    title = models.CharField(max_length=100, default='')
    seo_title = models.CharField(max_length=100, default='')
    seo_description = models.CharField(max_length=100, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    date_created = models.DateTimeField(auto_now=True)
    cover_image = models.ForeignKey('GalleryImage', default=None, blank=True, null=True, related_name='cover_image')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/people/%i/" % self.id

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery)
    gallery_image = models.ImageField(upload_to='media/gallery/', blank=True, null=True)

    def __unicode__(self):
        return self.gallery_image.name

    class Meta:
        verbose_name = 'Изображение в галерее'
        verbose_name_plural = 'Изображения в галерее'


class Question(models.Model):
    published = models.BooleanField(default=False)
    text = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Employee(models.Model):
    name = models.CharField(max_length=50, null=False)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    published = models.BooleanField(default=True)
    position = models.TextField()
    text = models.TextField()
    image = models.ForeignKey(Image, related_name='employees', default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


def email_question(sender, instance, created, **kwargs):
    if created:
        send_mail(
            u'Новый вопрос на сайте zavod',
            u'Поступил новый вопрос. ' \
            u'Вы можете зайти в раздел администрирования и ответить на него. ' \
            u'Текст вопроса:\n\n{}'.format(instance.text),
            'from@example.com',
            EMAILS_FOR_FAQ,
            fail_silently=True,
        )

post_save.connect(email_question, sender=Question, dispatch_uid="email_question")
