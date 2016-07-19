from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^catalog/[-\w]+/$', views.catalog_category, name='catalog_category'),
    url(r'^catalog/[-\w]+/[-\w]+/$', views.product_or_products, name='product_or_products'),
    url(r'^catalog/[-\w]+/[-\w]+/[-\w]+/$', views.product_or_products, name='product_or_products'),
    url(r'^prajjsy/$', views.prajjsy, name='prajjsy'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^articles/[-\w]+/$', views.articles_detail, name='articles_detail'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^dostavka/$', views.dostavka, name='dostavka'),
    url(r'^dokumentatsija/$', views.dokumentatsija, name='dokumentatsija'),
]
