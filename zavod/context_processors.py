from zavod.models import News
from zavod.models import Gallery
from zavod.models import Product


def news_for_bottom(request):
    news_for_bottom = News.objects.order_by('date_created').first()
    return {'news_for_bottom': news_for_bottom}


def product_for_bottom(request):
    product_for_bottom = Product.objects.filter(published=True).first()
    return {'product_for_bottom': product_for_bottom}


def media_for_bottom(request):
    media_for_bottom = Gallery.objects.filter(published=True).first()
    return {'media_for_bottom': media_for_bottom}