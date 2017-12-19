from django.shortcuts import render,HttpResponse,redirect
from Blog import models
from Blog.auth.auth import auth
# Create your views here.
from datetime import datetime
#分页
from utils.pagination import Page
from django.urls import reverse


@auth
def index(request):
    return render(request, 'BM_index.html')

@auth
def articles(request,*args,**kwargs):
    # print(kwargs)
    #获取当前url
    # print(request.path_info)
    # from django.urls import reverse
    # url = reverse('articles',kwargs=kwargs)
    # print(url)


    # article_type_list = models.ArticleType.objects.all()
    # 组合搜索
    article_type_list = models.Article.type_choices
    category_list = models.Category.objects.filter(blog_id=request.session['user_info']['blog__nid'])
    blog = models.Blog.objects.filter(site=request.session['user_info']['blog__site']).select_related('user').first()

    #组合搜索
    c = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            c[k]=v
    # 指定查找所有属于该博主的博文
    c['blog'] = blog
    data_count = models.Article.objects.filter(**c).count()
    articles = models.Article.objects.filter(**c).order_by('-create_time').select_related('blog')

    #分页
    current_page = request.GET.get('p', 1)  # 获取对应get数据p: href="/user_list/?p=%s
    current_page = int(current_page)
    page = Page(current_page,len(articles),7)
    data = articles[page.start:page.end]  # 列表切片
    page_str = page.page_str(reverse('articles', kwargs=kwargs))
    return render(request,'BM_articles.html',{'arts':data,
                                              'page_str':page_str,
                                              'article_type_list':article_type_list,
                                              'category_list':category_list,
                                              'arg_dic':kwargs,
                                              'data_count':data_count,})


@auth
def edit_article(request,nid):
    if request.method == 'GET':
        obj = models.Article.objects.filter(nid=nid).first()
        obj_detail = models.ArticleDetail.objects.filter(article=obj).first()
        # print(obj.title,obj.summary,obj_detail.content)
        blog_id = request.session['user_info']['blog__nid']
        article_type_list = models.Article.type_choices
        category_list = models.Category.objects.filter(blog_id=blog_id)
        return render(request,'BM_edit.html',{'obj':obj,'obj_detail':obj_detail,
                                              'article_type_list': article_type_list,
                                              'category_list': category_list,
                                              })

    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        article_type_id = request.POST.get('article_type_id')
        category_id = request.POST.get('category_id')
        blog_id = request.session['user_info']['blog__nid']
        models.Article.objects.filter(nid = nid).update(title=title,summary=summary,
                                                        article_type_id=article_type_id,
                                                        category_id=category_id,)
        obj = models.Article.objects.filter(nid=nid).first()
        obj_detail = models.ArticleDetail.objects.filter(article=obj).update(content=content)
        return redirect('bm/edit-article-%s/' % nid)


@auth
def add(request):
    if request.method == 'GET':
        blog_id = request.session['user_info']['blog__nid']
        article_type_list = models.Article.type_choices
        category_list = models.Category.objects.filter(blog_id=blog_id)
        return render(request, 'BM_add.html',{'article_type_list': article_type_list,
                                              'category_list': category_list,})
    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        article_type_id = request.POST.get('article_type_id')
        category_id = request.POST.get('category_id')
        blog_id = request.session['user_info']['blog__nid']
        obj = models.Article.objects.create(title=title,summary=summary,blog_id=blog_id,article_type_id=article_type_id,
                                            category_id=category_id,create_time=datetime.now())
        models.ArticleDetail.objects.create(content=content,article = obj)

        return redirect('/bm/add/')

@auth
def delete(request):
    if request.method == 'GET':
        url = request.path_info
        print(url)
        nid = request.GET.get('nid')
        obj = models.Article.objects.filter(nid=nid).delete()
        aa = models.ArticleDetail.objects.filter(article=obj).delete()
        return HttpResponse('200')


@auth
def mydetail(request):
    if request.method =='GET':
        nid = request.session['user_info']['nid']
        obj = models.UserInfo.objects.filter(nid=nid).first()
        blog = models.Blog.objects.filter(user = obj).first()
        return render(request,'BM_mydetail.html',{'obj':obj,'blog':blog})
    if request.method == 'POST':
        nid = request.session['user_info']['nid']
        nick = request.POST.get('nickname')
        blogsite = request.POST.get('blogUrl')
        blogTitle = request.POST.get('blogTitle')
        blogTheme = request.POST.get('blogTheme')
        obj = models.UserInfo.objects.filter(nid=nid)
        models.UserInfo.objects.filter(nid=nid).update(nickname= nick)
        #重设sesion保持site,和nickname同步
        models.Blog.objects.filter(user=obj).update(title = blogTitle,site=blogsite,theme=blogTheme)
        ses = request.session['user_info']
        request.session['user_info'] = ''
        ses['blog__site'] = blogsite
        ses['nickname'] = nick
        request.session['user_info'] = ses
        return redirect('/bm/mydetail/')

def upload_avatar(request):
    if request.method == 'POST':
        img = request.FILES.get('avatar_img')
        print(img.name)
        import os
        img_path = os.path.join('static/imgs/',img.name)
        with open(img_path,'wb') as f:
            for i in img.chunks():
                f.write(i)

        return HttpResponse(img_path)




@auth
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """

    return render(request, 'BM_tag.html')

@auth
def category(request):
    '''
    博主个人文章分类管理
    '''

    blog_id = request.session['user_info']['blog__nid']
    obj = models.Article.objects.filter(blog_id = blog_id)
    category = models.Category.objects.filter(blog_id = blog_id)
    category_list = []
    if obj.exists():
        for i in category:
            m = 0
            for n in obj:
                if i.nid == n.category_id:
                    m += 1
            category_list.append([i.title,m,i])
    else:
        for i in category:
            category_list.append([i.title,0,i])
    # print(category_list)

    #分页
    current_page = request.GET.get('p', 1)  # 获取对应get数据p: href="/user_list/?p=%s
    current_page = int(current_page)
    page_num = 8
    page = Page(current_page,len(category_list),page_num)
    data = category_list[page.start:page.end]  # 列表切片
    page_str = page.page_str('/bm/category/')


    return render(request,'BM_category.html',{'category':data,
                                              'page_str': page_str,

                                              })

@auth
def add_category(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        blog_id = request.session['user_info']['blog__nid']
        models.Category.objects.create(blog_id=blog_id,title=data)
        return HttpResponse(200)

@auth
def delete_category(request):
    if request.method == 'POST':
        data = request.POST.get('nid')
        blog_id = request.session['user_info']['blog__nid']
        models.Category.objects.filter(nid=data).delete()
        return HttpResponse(200)