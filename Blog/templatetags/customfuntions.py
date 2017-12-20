# -*- coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def subnum(a1,a2):
    return a2-a1

@register.filter
def customdegression(n):
    return n-10

@register.filter
def addnum(a1,a2):
    return a1+a2

