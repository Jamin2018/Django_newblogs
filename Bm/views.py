from django.shortcuts import render,HttpResponse,redirect
from Blog import models
from Blog.auth.auth import auth
# Create your views here.
from datetime import datetime

@auth
def index(request):
    return render(request, 'BM_index.html')

@auth
def articles(request):
    blog = models.Blog.objects.filter(site=request.session['user_info']['blog__site']).select_related('user').first()
    articles = models.Article.objects.filter(blog=blog).order_by('-create_time')
    return render(request,'BM_articles.html',{'arts':articles})


@auth
def edit_article(request,nid):
    if request.method == 'GET':
        obj = models.Article.objects.filter(nid=nid).first()
        obj_detail = models.ArticleDetail.objects.filter(article=obj).first()
        # print(obj.title,obj.summary,obj_detail.content)

        return render(request,'BM_edit.html',{'obj':obj,'obj_detail':obj_detail})

    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        models.Article.objects.filter(nid = nid).update(title=title,summary=summary)
        obj = models.Article.objects.filter(nid=nid).first()
        obj_detail = models.ArticleDetail.objects.filter(article=obj).update(content=content)
        return redirect('bm/edit-article-%s' % nid)


@auth
def add(request):
    if request.method == 'GET':
        return render(request, 'BM_add.html')
    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        blog_id = request.session['user_info']['blog__nid']
        obj = models.Article.objects.create(title=title,summary=summary,blog_id=blog_id,create_time=datetime.now())
        models.ArticleDetail.objects.create(content=content,article = obj)

        return render(request, 'BM_add.html')

@auth
def delete(request):
    if request.method == 'POST':
        nid = request.POST.get('nid')
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
        obj = models.UserInfo.objects.filter(nid=nid)
        models.UserInfo.objects.filter(nid=nid).update(nickname= nick)
        #重设sesion保持site,和nickname同步
        models.Blog.objects.filter(user=obj).update(title = blogTitle,site=blogsite)
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

