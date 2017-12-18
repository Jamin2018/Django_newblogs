from django.db import models

# Create your models here.


class UserInfo(models.Model):
    '''
    用户表
    '''
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    nickname = models.CharField(verbose_name='昵称',max_length=32)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    avatar = models.ImageField(verbose_name='头像',null=True)

    create_time = models.DateTimeField(verbose_name='注册时间',auto_now_add=True)

    # fans = models.ManyToManyField(verbose_name='被粉数',
    #                               to='UserInfo',
    #                               through='UserFans',
    #                               related_name='f',
    #                               through_fields=('user','follower'))

class Blog(models.Model):
    '''
    博客信息
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    user = models.OneToOneField(to='UserInfo',to_field='nid')


class UserFans(models.Model):
    '''
    互粉关系表
    '''
    pass

class Category(models.Model):
    '''
    博主个人文章分类
    '''
    pass

class ArticleDetail(models.Model):
    '''
    文章内容
    '''
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',to='Article',to_field='nid')

class Article(models.Model):
    '''
    文章详细
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=128)
    summary = models.CharField(verbose_name='文章简介',max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid')
    # category = models.ForeignKey(verbose_name='文章类型',to='Category',to_field='nid',null=True)


class UpDown(models.Model):
    '''
    文章顶或踩
    '''
    article = models.ForeignKey(verbose_name='点赞的文章',to='Article',to_field='nid')
    user = models.ForeignKey(verbose_name='赞或踩的用户',to='UserInfo',to_field='nid')
    up = models.BooleanField(verbose_name='是否赞过')

    class Meta:
        unique_together = [
            ('article','user')
        ]


class Comment(models.Model):
    '''
    评论
    '''
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255,null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')

class Tag(models.Model):
    pass
