from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


GENDER_CHOICES = [
    ('M', '男'),
    ('F', '女'),
    ('U', '保密'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name='头像')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U', verbose_name='性别')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='城市')
    occupation = models.CharField(max_length=100, null=True, blank=True, verbose_name='工作')
    bio = models.TextField(max_length=500, null=True, blank=True, verbose_name='个人简介')

    def __str__(self):
        return f'{self.get_display_name()} 的资料'

    def get_display_name(self):
        """优先返回昵称，否则返回 username"""
        return self.nickname if self.nickname else self.user.username

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """用户创建时自动创建资料，nickname 默认为 username"""
    if created:
        UserProfile.objects.get_or_create(user=instance, defaults={'nickname': instance.username})
    else:
        # 保存时如果 profile 不存在则创建
        UserProfile.objects.get_or_create(user=instance)


class Category(models.Model): 
    name = models.CharField('分类', max_length=128)
    name_en = models.CharField('English Name', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_name(self):
        from django.utils.translation import get_language
        lang = get_language()
        if lang == 'en' and self.name_en:
            return self.name_en
        return self.name

    class Meta: 
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    name = models.CharField('标签', max_length=128)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

class Entry(models.Model):
    title = models.CharField('标题', max_length=128)
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog_img',null=True,blank=True,verbose_name='博客配图')
    body = models.TextField('正文',)
    abstract = models.TextField('摘要',max_length=256,null=True,blank=True)
    visitors = models.PositiveIntegerField('访问量',default=0)
    category = models.ForeignKey('Category', verbose_name='博客分类', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag',verbose_name='标签')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    modifyed_time = models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = '博客正文'
        verbose_name_plural = verbose_name
    
    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'blog_id': self.id})

    def increase_visitor_count(self):
        #访问量加1
        self.visitors += 1
        self.save(update_fields=['visitors'])   

    

    





