# -*- coding: utf-8 -*-
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import User, UserManager, AbstractBaseUser
from zavod.constants import POPULAR_TYPE_CHOICES, HIT, SUBSCRIPTION_TYPE, SUBSCRIPTION_TYPE_CHOICES
from zavod.templatetags.extras import get_full_product_path
from zt.settings import EMAILS_FOR_FAQ


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

    def image_tag(self):
        return u'<img src="{}" />'.format(self.image.url)

    image_tag.short_description = 'Изображение'
    image_tag.allow_tags = True

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class News(models.Model):
    published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, default='', unique=True)
    preview_post = models.TextField()
    text = RichTextUploadingField()
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=1000)
    seo_title = models.CharField(max_length=200, default='')
    seo_description = models.CharField(max_length=1000, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='news', default=None, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name='news', default=None, null=True, blank=True)
    author = models.TextField(default='')

    def __unicode__(self):
        return self.title

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
    text = RichTextUploadingField(default='')
    images = models.ManyToManyField(Image, related_name='categories', default=None, null=True, blank=True)
    files = models.ManyToManyField(File, related_name='categories', default=None, null=True, blank=True)
    galleries = models.ManyToManyField('Gallery', related_name='categories', default=None, null=True, blank=True)
    price_list = models.FileField(upload_to='media/price_lists/', blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Property(models.Model):
    title = models.CharField(max_length=200, default='')
    units = models.CharField(max_length=200, default='')
    slug = models.CharField(max_length=200, default='')
    filterable = models.BooleanField(default=0)

    def __unicode__(self):
        return u'{}, {}'.format(self.title, self.units)

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'


class Product(models.Model):
    published = models.BooleanField(default=True)
    is_black_friday = models.BooleanField(default=False)
    black_friday_discount = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='')
    category = models.ForeignKey(CategoryProduct, null=True)
    product_text = RichTextUploadingField()
    title = models.CharField(max_length=200, default='')
    seo_title = models.CharField(max_length=300, default='')
    seo_description = models.CharField(max_length=300, default='')
    seo_keywords = models.CharField(max_length=300, default='')
    images = models.ManyToManyField(Image, related_name='products', default=None, null=True, blank=True)
    image_in_description = models.ForeignKey(Image, related_name='product_description', default=None, null=True, blank=True)
    related_products = models.ManyToManyField('Product', related_name='related_to', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?tab=review".format(reverse('catalog_category', args=[get_full_product_path(self)]))

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductProperty(models.Model):
    property = models.ForeignKey(Property, related_name='products')
    product = models.ForeignKey(Product, related_name='properties')
    value = models.CharField(max_length=200, default='')

    def __unicode__(self):
        return u'{} - {}'.format(self.property.title, self.value)

    class Meta:
        verbose_name = 'Свойство продукта'
        verbose_name_plural = 'Свойства продуктов'


class PopularProduct(models.Model):
    category = models.ForeignKey(CategoryProduct, related_name='popularproduct')
    product = models.ForeignKey(Product, related_name='popular')
    type = models.IntegerField(choices=POPULAR_TYPE_CHOICES, default=HIT)

    def __unicode__(self):
        return u'{}: {} ({})'.format(self.category.name, self.product.name, self.type)

    class Meta:
        verbose_name = 'Популярный продукт в категории'
        verbose_name_plural = 'Популярные продукты в категориях'


class Article(models.Model):
    published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, default='', unique=True)
    preview_post = models.TextField()
    text = RichTextUploadingField()
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=1000)
    seo_title = models.CharField(max_length=200, default='')
    seo_description = models.CharField(max_length=1000, default='')
    seo_keywords = models.CharField(max_length=100, default='')
    author = models.TextField(max_length=200, default='')
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='articles', default=None, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name='articles', default=None, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='articles', default=None, null=True, blank=True)
    category = models.ManyToManyField(CategoryProduct, related_name='articles', default=None, null=True, blank=True)

    def __unicode__(self):
        return self.title

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
    cover_image = models.ImageField(upload_to='media/gallery/', blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/people/%i/" % self.id

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='galleryimage')
    gallery_image = models.ImageField(upload_to='media/gallery/', blank=True, null=True)

    def __unicode__(self):
        return self.gallery_image.name

    class Meta:
        verbose_name = 'Изображение в галерее'
        verbose_name_plural = 'Изображения в галерее'


class GalleryVideo(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='galleryvideo')
    video_url = models.CharField(max_length=500, default='', blank=True, null=True)
    cover_image = models.ImageField(upload_to='media/gallery/', blank=True, null=True)
    is_otzyv = models.BooleanField(default=False)

    def __unicode__(self):
        return self.video_url

    class Meta:
        verbose_name = 'Видео в галерее'
        verbose_name_plural = 'Видео в галерее'


class Question(models.Model):
    published = models.BooleanField(default=False)
    text = models.TextField()
    answer = models.TextField()
    type = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Department(models.Model):
    title = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Employee(models.Model):
    email = models.EmailField(max_length=50, default='')
    name = models.CharField(max_length=50, null=False)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    published = models.BooleanField(default=True)
    position = models.TextField()
    text = models.TextField()
    image = models.ForeignKey(Image, related_name='employees', default=None, null=True, blank=True)
    department = models.ForeignKey(Department, related_name='employees', default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Subscription(models.Model):
    email = models.EmailField(max_length=50, default='')
    type = models.IntegerField(choices=SUBSCRIPTION_TYPE_CHOICES, default=SUBSCRIPTION_TYPE[u'Нет'])

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


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
