from django.db import models
from django.utils import timezone


class Article(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, default='', unique=True)
	preview_post = models.TextField(max_length = 200)
	text = models.TextField()
	date_created = models.DateTimeField(default=timezone.now)
	title = models.CharField(max_length = 100, default='')
	seo_title = models.CharField(max_length = 100, default='')
	seo_description = models.CharField(max_length = 100, default='')
	seo_keywords = models.CharField(max_length = 100, default='')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Статья'
		verbose_name_plural = 'Статьи'

class ArticleImage(models.Model):
	article = models.ForeignKey(Article)
	article_image = models.FileField(upload_to='media/articles/', blank=True, null=True)


class CategoryProduct(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length = 100, default='', unique=True)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Категория продуктов'
		verbose_name_plural = 'Категории продуктов'

class Product(models.Model):
	name = models.CharField(max_length = 100, default='')
	slug = models.SlugField(max_length = 100, default='', unique=True)
	product_category = models.ForeignKey(CategoryProduct)
	product_text = models.TextField()
	title = models.CharField(max_length = 100, default='')
	seo_title = models.CharField(max_length = 100, default='')
	seo_description = models.CharField(max_length = 100, default='')
	seo_keywords = models.CharField(max_length = 100, default='')
	def __str__(self):
	    return self.name
	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'

class SubProduct(models.Model):
	name = models.CharField(max_length = 100, default='')
	product = models.ForeignKey(Product)
	slug = models.SlugField(max_length = 100, default='', unique=True)
	# product_category = models.ForeignKey(CategoryProduct)
	product_text = models.TextField()
	title = models.CharField(max_length = 100, default='')
	seo_title = models.CharField(max_length = 100, default='')
	seo_description = models.CharField(max_length = 100, default='')
	seo_keywords = models.CharField(max_length = 100, default='')
	def __str__(self):
	    return self.name
	class Meta:
		verbose_name = 'Вложенный продукт'
		verbose_name_plural = 'Вложенные продукты'

class ProductImage(models.Model):
	article = models.ForeignKey(Product)
	product_image = models.FileField(upload_to='media/products/', blank=True, null=True)