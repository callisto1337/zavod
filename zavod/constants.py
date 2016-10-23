# -*- coding: utf-8 -*-

SPECIAL_FILTER_PARAMS = {
    u'Диапазон температур_max': ur'- ([\-, \+]\d+)°C',
    u'Диапазон температур_min': ur'([\-, \+]\d+)°C - ',
}

HIT = 0
SALE = 1
NEW = 2
POPULAR_TYPE_CHOICES = (
    (HIT, u'Хит'),
    (SALE, u'Скидка!'),
    (NEW, u'Новинка'),
)

SUBSCRIPTION_TYPE = {
    u'Нет': 0,
    u'Новости': 1,
    u'Статьи': 2,
}
SUBSCRIPTION_TYPE_CHOICES = (
    (0, u'Нет'),
    (1, u'Новости'),
    (2, u'Статьи'),
)

