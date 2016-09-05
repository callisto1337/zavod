from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', views.main, name='main'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^catalog/(?P<category_slug>[-\w]+)/$', views.catalog_category, name='catalog_category'),
    url(r'^catalog/(?P<parent_category_slug>[-\w]+)/(?P<category_slug>[-\w]+)/$', views.catalog_category, name='catalog_category_inside'),
    url(r'^catalog/(?P<parent_category_slug>[-\w]+)/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', views.product_or_products, name='product_or_products'),
    url(r'^product/(?P<slug>[-\w]+)/$', views.get_product, name='get_product'),
    url(r'^prajjsy/$', views.prajjsy, name='prajjsy'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^articles/(?P<article_slug>[-\w]+)/$', views.articles_detail, name='articles_detail'),
    url(r'^articles/page-(?P<page_number>[0-9]+)/$', views.articles_page, name='articles_page'),
    url(r'^articles/tag/(?P<tag>[-\w]+)/$', views.articles_tag, name='articles_tag'),
    url(r'^articles/tag/(?P<tag>[-\w]+)/page-(?P<page_number>[0-9]+)/$', views.articles_tag_page,
        name='articles_tag_page'),
    url(r'^news/$', views.news, name='news'),
    url(r'^news/(?P<news_slug>[-\w]+)/$', views.news_detail, name='news_detail'),
    url(r'^news/page-(?P<page_number>[0-9]+)/$', views.news_page, name='news_page'),
    url(r'^news/tag/(?P<tag>[-\w]+)/$', views.news_tag, name='news_tag'),
    url(r'^news/tag/(?P<tag>[-\w]+)/page-(?P<page_number>[0-9]+)/$', views.news_tag_page,
        name='news_tag_page'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^dostavka/$', views.dostavka, name='dostavka'),
    url(r'^dostavka/mezhdunarodnaja-dostavka/$', views.mezhdunarodnaja_dostavka, name='mezhdunarodnaja_dostavka'),
    url(r'^geografija-prodazh/$', views.geografija_prodazh, name='geografija_prodazh'),
    url(r'^dokumentatsija/$', views.dokumentatsija, name='dokumentatsija'),
    url(r'^dokumentatsija/razreshenie-na-primenenie/$', views.razreshenie_na_primenenie,
        name='razreshenie_na_primenenie'),
    url(r'^dokumentatsija/sertifikaty/$', views.sertifikaty, name='sertifikaty'),
    url(r'^dokumentatsija/tekhnicheskaja-dokumentatsija/$', views.tekhnicheskaja_dokumentatsija,
        name='tekhnicheskaja_dokumentatsija'),
    url(r'^dokumentatsija/zachem-nuzhna-dokumentatsija/$', views.zachem_nuzhna_dokumentatsija,
        name='zachem_nuzhna_dokumentatsija'),
    url(r'^dokumentatsija/tovarnye-znaki/$', views.tovarnye_znaki, name='tovarnye_znaki'),
    url(r'^dokumentatsija/tovarnye-znaki/mezhdunarodnye-tovarnye-znaki/$', views.mezhdunarodnye_tovarnye_znaki,
        name='mezhdunarodnye_tovarnye_znaki'),
    url(r'^dokumentatsija/tovarnye-znaki/tovarnyjj-znak-zachem-on/$', views.tovarnyjj_znak_zachem_on,
        name='tovarnyjj_znak_zachem_on'),
    url(r'^photogallery/$', views.photogallery, name='photogallery'),
    url(r'^photogallery/(?P<photogallery_slug>[-\w]+)/$', views.photogallery_detail, name='photogallery_detail'),
    url(r'^photogallery/(?P<photogallery_slug>[-\w]+)/page-(?P<page_number>[0-9]+)/$', views.photogallery_detail_page, name='photogallery_detail_page'),
    url(r'^news/$', views.news, name='news'),
    url(r'^about/$', views.about, name='about'),
    url(r'^about/otzyvy/$', views.otzyvy, name='otzyvy'),
    url(r'^partnery/$', views.partnery, name='partnery'),
    url(r'^proizvodstvo-zavoda-triumf/$', views.proizvodstvo_zavoda_triumf, name='proizvodstvo_zavoda_triumf'),
    url(r'^prajjsy/gibkaja-sistema-skidok/$', views.gibkaja_sistema_skidok, name='gibkaja_sistema_skidok'),
]
