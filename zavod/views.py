# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect

from .models import Article, CategoryProduct, Product, SubCategoryProduct


def main(request):
	return render(request, 'zavod/main.html')


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
	return render(request, 'zavod/dokumentatsija.html')


def razreshenie_na_primenenie(request):
	return render(request, 'zavod/razreshenie_na_primenenie.html')


def sertifikaty(request):
	return render(request, 'zavod/sertifikaty.html')


def tovarnye_znaki(request):
	return render(request, 'zavod/tovarnye_znaki.html')


def mezhdunarodnye_tovarnye_znaki(request):
	return render(request, 'zavod/mezhdunarodnye_tovarnye_znaki.html')


def tovarnyjj_znak_zachem_on(request):
	return render(request, 'zavod/tovarnyjj_znak_zachem_on.html')


def tekhnicheskaja_dokumentatsija(request):
	return render(request, 'zavod/tekhnicheskaja_dokumentatsija.html')


def zachem_nuzhna_dokumentatsija(request):
	return render(request, 'zavod/zachem_nuzhna_dokumentatsija.html')


def photogallery(request):
	return render(request, 'zavod/photogallery.html')


def news(request):
	return render(request, 'zavod/news.html')


def about(request):
	return render(request, 'zavod/about.html')


def otzyvy(request):
	return render(request, 'zavod/otzyvy.html')


def partnery(request):
	return render(request, 'zavod/partnery.html')


def proizvodstvo_zavoda_triumf(request):
	return render(request, 'zavod/proizvodstvo_zavoda_triumf.html')


def gibkaja_sistema_skidok(request):
	return render(request, 'zavod/gibkaja_sistema_skidok.html')


def articles(request):
	articles = Article.objects.all().filter(published=True)[:5]
	return render(request, 'zavod/articles.html', {'articles': articles})


def articles_detail(request):
	path_article = str(request.path.replace('articles', '').replace('/', ''))
	try:
		int(path_article)
		article = get_object_or_404(Article, pk=path_article)
		return HttpResponsePermanentRedirect(article.slug)
	except:
		article = get_object_or_404(Article, slug=path_article)
		return render(request, 'zavod/articles_detail.html', {'article': article})


def catalog(request):
	category_products = CategoryProduct.objects.all().filter(published=True)[:5]
	return render(request, 'zavod/catalog.html', {'category_products': category_products})


def catalog_category(request):
	path_catalog = request.path.replace('/', ' ').split()
	category = get_object_or_404(CategoryProduct, slug=path_catalog[1])
	subcategory = SubCategoryProduct(slug=path_catalog[1])

	if SubCategoryProduct.objects.all().filter(category=category):
		title = 'Вложенные категории'
		subcategories = SubCategoryProduct.objects.all().filter(category=category, published=True)
		return render(request, 'zavod/catalog_category.html', {'subcategories': subcategories, 'title': title})
	else:
		title = 'Список продуктов'
		parent = get_object_or_404(CategoryProduct, slug=path_catalog[1])
		products = Product.objects.all().filter(category=parent, published=True)
		return render(request, 'zavod/catalog_category.html', {'products': products, 'parent': parent, 'title': title})


def product_or_products(request):
	path_product = request.path.replace('/', ' ').split()
	category = get_object_or_404(CategoryProduct, slug=path_product[1])

	if len(path_product) == 3:
		if Product.objects.all().filter(slug=path_product[2]):
			product = Product.objects.all().filter(slug=path_product[2], published=True)
			return render(request, 'zavod/product.html', {'product': product})
		else:
			title = 'Список продуктов во вложенной категории'
			subcategory_id = get_object_or_404(SubCategoryProduct, slug=path_product[2])
			products = Product.objects.all().filter(subcategory=subcategory_id, published=True)
			return render(request, 'zavod/catalog_category.html', {'products': products, 'title': title})
	else:
		subcategory = get_object_or_404(SubCategoryProduct, slug=path_product[2])
		product = get_object_or_404(Product, slug=path_product[3])
		return render(request, 'zavod/product.html', {'product': product})
