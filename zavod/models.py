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

class SubCategoryProduct(models.Model):
	name = models.CharField(max_length = 100, default='')
	category = models.ForeignKey(CategoryProduct)
	slug = models.SlugField(max_length = 100, default='', unique=True)

	def __str__(self):
	    return self.name
	class Meta:
		verbose_name = 'Вложенная категория'
		verbose_name_plural = 'Вложенные категории'

class Product(models.Model):
	list_display = ('name', 'slug')

	name = models.CharField(max_length = 100, default='')
	slug = models.SlugField(max_length = 100, default='', unique=True)
	category = models.ForeignKey(CategoryProduct)
	subcategory = models.ForeignKey(SubCategoryProduct, null=True)
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

class ProductImage(models.Model):
	article = models.ForeignKey(Product)
	product_image = models.FileField(upload_to='media/products/', blank=True, null=True)