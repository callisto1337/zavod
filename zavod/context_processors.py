from django.contrib.auth.forms import AuthenticationForm
from zavod.forms import CallMeForm, CustomUserCreationForm
from zavod.models import News
from zavod.models import Gallery
from zavod.models import Product


def news_for_bottom(request):
    news_for_bottom = News.objects.order_by('date_created').first()
    return {'news_for_bottom': news_for_bottom}


def product_for_bottom(request):
    product_for_bottom = Product.objects.filter(published=True).exclude(category=None).order_by('?').first()
    return {'product_for_bottom': product_for_bottom}


def media_for_bottom(request):
    media_for_bottom = Gallery.objects.filter(published=True).first()
    return {'media_for_bottom': media_for_bottom}


def black_friday_product(request):
    black_friday_product = Product.objects.\
        filter(published=True, is_black_friday=True).\
        exclude(category=None).\
        order_by('?').first()
    return {'black_friday_product': black_friday_product}


def callme_form(request):
    callme_form = CallMeForm()
    return {
        'callme_form': callme_form,
        'callme_form_url': unicode(request.path)
    }


def log_in_form(request):
    log_in_form = AuthenticationForm()
    return {
        'log_in_form': log_in_form,
        'log_in_form_url': unicode(request.path)
    }


def registration_form(request):
    registration_form = CustomUserCreationForm()
    return {
        'registration_form': registration_form,
        'registration_form_url': unicode(request.path)
    }
