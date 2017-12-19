from django.shortcuts import render,HttpResponse,redirect
from Blog import models
import json
#分页
from utils.pagination import Page
from django.urls import reverse
# Create your views here.

def index(request,**kwargs):
    if request.method =='GET':
        article_type_list = models.Article.type_choices

        c = {}
        for k,v in kwargs.items():
            kwargs[k] = int(v)
            if v !='0':
                c[k] = v
        all_articles = models.Article.objects.filter(**c).order_by('-create_time')
        hot_articles = models.Article.objects.filter().order_by('-up_count')[:5]
        read_articles = models.Article.objects.filter().order_by('-read_count')[:5]

        # 分页
        current_page = request.GET.get('p', 1)  # 获取对应get数据p: href="/user_list/?p=%s
        current_page = int(current_page)
        page_num = 10
        page = Page(current_page, len(all_articles), page_num)
        data = all_articles[page.start:page.end]  # 列表切片
        page_str = page.page_str('/')
        return render(request,'index.html',{'all_articles':data,
                                            'page_str': page_str,
                                            'hot':hot_articles,
                                            'read':read_articles,
                                            'article_type_list': article_type_list,
                                            'arg_dict':kwargs,
                                            })

def article_up(request):
    if request.method == 'POST':
        # print(request.POST.get('obj'))
        ret = {}
        try:
            nid = request.POST.get('nid')
            uid = request.session['user_info']['nid']
            if not models.UpDown.objects.filter(article_id=nid,user_id=uid):
                models.UpDown.objects.create(article_id=nid,user_id=uid,up=True)
                # 点赞加一
                obj = models.Article.objects.filter(nid=nid)
                n = obj.first().up_count
                n += 1
                obj.update(up_count=n)
                a = models.Article.objects.filter(nid=nid).first().up_count
                ret['num_up'] = a
                b = models.Article.objects.filter(nid=nid).first().down_count
                ret['num_down'] = b
                ret['state'] = 1
            else:
                if  models.UpDown.objects.filter(article_id=nid,user_id=uid,up=False):
                    models.UpDown.objects.filter(article_id=nid,user_id=uid).update(up=True)
                    obj = models.Article.objects.filter(nid=nid)
                    #踩减一
                    n = obj.first().down_count
                    n -= 1
                    obj.update(down_count=n)
                    # 赞加一
                    n = obj.first().up_count
                    n += 1
                    obj.update(up_count=n)
                    a = models.Article.objects.filter(nid=nid).first().up_count
                    ret['num_up'] = a
                    b = models.Article.objects.filter(nid=nid).first().down_count
                    ret['num_down'] = b
                    ret['state'] = 1
        except:
            # ret['state'] = 0
            pass
        return HttpResponse(json.dumps(ret))

def article_down(request):
    if request.method == 'POST':
        ret = {'status': 0,}
        try:
            nid = request.POST.get('nid')
            uid = request.session['user_info']['nid']
            if not models.UpDown.objects.filter(article_id=nid, user_id=uid):
                models.UpDown.objects.create(article_id=nid,user_id=uid,up=False)
                # 踩加一
                obj = models.Article.objects.filter(nid=nid)
                n = obj.first().down_count
                n += 1
                obj.update(down_count=n)
                n = models.Article.objects.filter(nid=nid).first().down_count
                ret['num_down'] = n
                n = models.Article.objects.filter(nid=nid).first().up_count
                ret['num_up'] = n
                ret['state'] = 1
            else:
                if models.UpDown.objects.filter(article_id=nid, user_id=uid, up=True):
                    models.UpDown.objects.filter(article_id=nid,user_id=uid).update(up=False)
                    obj = models.Article.objects.filter(nid=nid)
                    #踩加一
                    n = obj.first().down_count
                    n += 1
                    obj.update(down_count=n)
                    # 赞减一
                    n = obj.first().up_count
                    n -= 1
                    obj.update(up_count=n)
                    n = models.Article.objects.filter(nid=nid).first().down_count
                    ret['num_down'] = n
                    n = models.Article.objects.filter(nid=nid).first().up_count
                    ret['num_up'] = n
                    ret['state'] = 1
        except:
            # ret['state'] = 0
            pass
        return HttpResponse(json.dumps(ret))

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields,widgets

# 登录表单验证
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
                'nid','nickname','username','email','avatar','blog__nid','blog__site','blog__theme'
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

# 注册表单验证
class RegistrationForm( django_forms.Form):

    username = fields.CharField(
        #自定义部件
        widget=django_forms.TextInput(attrs={'class':'form-control'}),
        min_length=3,
        max_length=12,
        error_messages={
            'required': '用户名不能为空',
            'min_length': "用户名长度不能小于3个字符",
            'max_length': "用户名长度不能大于8个字符"
        }
    )

    nickname = fields.CharField(
        # 自定义部件
        widget=django_forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = fields.CharField(
        # 自定义部件
        widget=django_forms.TextInput(attrs={'class': 'form-control'}),
        min_length=3,
        max_length=20,
        error_messages={'required': '邮箱不能为空',
                        'min_length': "用户名长度不能小于3个字符",
                        'max_length': "用户名长度不能大于32个字符"}
    )
    password = fields.CharField(
        # 自定义部件
        widget=django_forms.TextInput(attrs={'class': 'form-control','type':'password'}),
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )


def registration(request):
    if request.method == 'GET':
        obj = RegistrationForm()
        return render(request,'registration.html',{'obj':obj})
    if request.method == 'POST':
        obj = RegistrationForm(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get('username')
            nickname = obj.cleaned_data.get('nickname')
            email = obj.cleaned_data.get('email')
            password = obj.cleaned_data.get('password')
            blog_title = username+'的个人博客'
            obj = models.UserInfo.objects.create(username=username,
                                                 nickname=nickname,
                                                 email=email,
                                                 password=password)
            models.Blog.objects.create(user=obj,site=username,title=blog_title)
            #注册后直接登录，所以重新赋值session
            user_info = models.UserInfo.objects.filter(email=email,password=password).values(
                'nid','nickname','username','email','avatar','blog__nid','blog__site'
            ).first()
            request.session['user_info'] = user_info
            return redirect('/')
        else:
            return render(request,'registration.html',{'obj':obj})

def out(request):
    request.session['user_info'] = ''
    return redirect('/')


from Blog.auth.auth import auth

# @auth
def blog(request,site,**kwargs):

    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    UserInfo = models.UserInfo.objects.filter(blog=blog).first()
    articles_count = models.Article.objects.filter(blog=blog).order_by('-create_time').count()
    read_articles = models.Article.objects.filter(blog=blog).order_by('-read_count')[:5]
    hot_articles = models.Article.objects.filter(blog=blog).order_by('-up_count')[:5]

    #组合搜索
    article_type_list = models.Article.type_choices
    category_list = models.Category.objects.filter(blog=blog)
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    c = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            c[k] = v
    # 指定查找所有属于该博主的博文
    c['blog'] = blog
    data_count = models.Article.objects.filter(**c).count()
    articles = models.Article.objects.filter(**c).order_by('-create_time').select_related('blog')


    # 分页
    current_page = request.GET.get('p', 1)  # 获取对应get数据p: href="/user_list/?p=%s
    current_page = int(current_page)
    page_num = 10
    page = Page(current_page, len(articles), page_num)
    data = articles[page.start:page.end]  # 列表切片
    page_str = page.page_str('/%s.html' % site)


    return render(request,'blog.html',{'userinfo':UserInfo,
                                       'blog':blog,
                                       'articles':data,
                                       'articles_count':articles_count,
                                       'page_str': page_str,
                                       'read':read_articles,
                                       'hot':hot_articles,
                                       'article_type_list': article_type_list,
                                       'category_list': category_list,
                                       'arg_dic': kwargs,
                                       'data_count': data_count,
                                       })



def myblog(request,site,nid):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    UserInfo = models.UserInfo.objects.filter(blog=blog).first()
    articles_count = models.Article.objects.filter(blog=blog).order_by('-create_time').count()
    new_articles = models.Article.objects.filter(blog=blog).order_by('-create_time')[:5]
    obj = models.Article.objects.filter(blog=blog,nid=nid).first()
    obj_content = models.ArticleDetail.objects.filter(article=obj).first()
    hot_articles = models.Article.objects.filter(blog=blog).order_by('-up_count')[:5]
    comment = models.Comment.objects.filter(article_id=nid).order_by('-create_time')

    #每次请求，阅读数加一
    # print(obj.read_count)
    n = obj.read_count
    n += 1
    models.Article.objects.filter(blog=blog,nid=nid).update(read_count=n)

    # 分页
    current_page = request.GET.get('p', 1)  # 获取对应get数据p: href="/user_list/?p=%s
    current_page = int(current_page)
    page = Page(current_page, len(comment), 7)
    data = comment[page.start:page.end]  # 列表切片
    page_str = page.page_str('/%s/%s.html' % (site,nid))

    return render(request, 'myblog.html', {'userinfo': UserInfo,
                                           'blog': blog,
                                           'articles_count': articles_count,
                                           'new': new_articles,
                                           'hot': hot_articles,
                                           'obj':obj,
                                           'obj_content':obj_content,
                                           'comment':data,
                                           'page_str': page_str,
                                           })

def comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        url = request.POST.get('article_url')
        nid = request.POST.get('article_nid')
        uid = request.session['user_info']['nid']
        n = models.Article.objects.filter(nid=nid).values('comment_count').first()['comment_count']
        n += 1
        models.Article.objects.filter(nid=nid).update(comment_count=n)
        models.Comment.objects.create(content=content,article_id=nid,user_id=uid)

        return redirect(url)

