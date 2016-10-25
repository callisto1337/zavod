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
