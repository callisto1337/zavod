from django import template
register = template.Library()


def mod(value, arg):
    return value % arg

register.filter('mod', mod)


def multiply(value, arg):
    return value * arg

register.filter('multiply', multiply)


def subtract(value, arg):
    return value - arg

register.filter('subtract', subtract)


def pages_set(value, arg):
    return value[(arg - 2):(arg + 1)]

register.filter('pages_set', pages_set)


def get_full_product_path(value):
    path = value.slug + '/'
    next_category = value.category
    while next_category:
        path = next_category.slug + '/' + path
        next_category = next_category.parent_id
    return path

register.filter('get_full_product_path', get_full_product_path)


def get_full_category_path(value):
    path = value.slug + '/'
    next_category = value.parent_id
    while next_category:
        path = next_category.slug + '/' + path
        next_category = next_category.parent_id
    return path

register.filter('get_full_category_path', get_full_category_path)
