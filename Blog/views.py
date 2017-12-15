from django.shortcuts import render,HttpResponse,redirect
from Blog import models
import json
# Create your views here.

def index(request):
    all_articles = models.Article.objects.filter().order_by('-create_time')
    return render(request,'index.html',{'all_articles':all_articles})


from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields,widgets

# 表单验证
class LoginForm( django_forms.Form):

    email = fields.CharField(
        min_length=3,
        max_length=20,
        error_messages={'required': '邮箱不能为空.', 'min_length': "用户名长度不能小于3个字符", 'max_length': "用户名长度不能大于32个字符"}
    )
    password = fields.CharField(
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    # rmb = fields.IntegerField(required=False)
    #
    # check_code = fields.CharField(
    #     error_messages={'required': '验证码不能为空.'}
    # )
    #
    # def clean_check_code(self):
    #     if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
    #         raise ValidationError(message='验证码错误', code='invalid')


def login(request):
    if request.method =='GET':
        return render(request,'login.html')
    if request.method =='POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email,password)
            user_info = models.UserInfo.objects.filter(email=email,password=password).values(
                'nid','nickname','username','email','avatar','blog__nid','blog__site'
            ).first()
            if not user_info:
                result['message'] = '邮箱不存在或密码错误'
            else:
                result['status']=True
                request.session['user_info'] = user_info
        else:
            print(form.errors)
            print(form.errors.as_json())
            result['message'] = '邮箱或密码错误'
        return HttpResponse(json.dumps(result))

def out(request):
    request.session['user_info'] = ''
    return redirect('/')


from Blog.auth.auth import auth

# @auth
def myblog(request,site):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    UserInfo = models.UserInfo.objects.filter(blog=blog).first()
    articles = models.Article.objects.filter(blog=blog).order_by('-create_time')
    read_articles = models.Article.objects.filter(blog=blog).order_by('-read_count')[:5]
    hot_articles = models.Article.objects.filter(blog=blog).order_by('-up_count')[:5]
    for i in read_articles:
        print(i.read_count)
    return render(request,'myblog.html',{'userinfo':UserInfo,
                                         'blog':blog,
                                         'articles':articles,
                                         'read':read_articles,
                                         'hot':hot_articles})


def test(request):
    return HttpResponse('ok')