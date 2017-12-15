# -*- coding:utf-8 -*-
from django.shortcuts import redirect

def auth(func):
    def inner(request,*args,**kwargs):
        if request.session.get('user_info'):
            # print(request.session['user_info'])
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return inner