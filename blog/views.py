from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _

from .models import Entry, Tag, UserProfile, Category
from .forms import RegisterForm, BlogForm, ProfileForm
import markdown


SORT_FIELD_WHITELIST = {
    'time': 'created_time',
    'visitors': 'visitors',
}


def index(request):
    blog_list = Entry.objects.all()
    search_query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    sort_field = request.GET.get('sort', 'time')
    sort_dir = request.GET.get('dir', 'desc')

    # 搜索逻辑：匹配用户、简介、标题、正文、标签
    if search_query:
        blog_list = blog_list.filter(
            Q(title__icontains=search_query) |
            Q(body__icontains=search_query) |
            Q(abstract__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(author__profile__bio__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()

    # 分类过滤
    if category_id and category_id.isdigit():
        blog_list = blog_list.filter(category__id=category_id)

    # 排序逻辑：使用白名单验证字段
    if sort_field in SORT_FIELD_WHITELIST:
        order_by_field = SORT_FIELD_WHITELIST[sort_field]
        if sort_dir == 'desc':
            order_by_field = f'-{order_by_field}'
        blog_list = blog_list.order_by(order_by_field)
    else:
        blog_list = blog_list.order_by('-created_time')

    categories = Category.objects.all()

    return render(request, 'blog/index.html', {
        'blog_list': blog_list,
        'search_query': search_query,
        'categories': categories,
        'current_category': category_id,
        'current_sort': sort_field,
        'current_dir': sort_dir,
    })

def detail(request,blog_id):
    blog = get_object_or_404(Entry, id=blog_id)

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])

    blog.body = md.convert(blog.body)
    blog.toc = md.toc
    blog.increase_visitor_count()

    return render(request,'blog/detail.html', {'blog': blog}) 


def user_login(request):
    if request.user.is_authenticated:
        return redirect('blog:blog_index')

    next_url = request.GET.get('next') or request.POST.get('next')
    form = AuthenticationForm(request=request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, _('登录成功。'))

        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect('blog:blog_index')

    return render(request, 'blog/login.html', {'form': form, 'next': next_url})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, _('你已安全登出。'))

    return redirect('blog:blog_index')

def user_register(request): 
    if request.user.is_authenticated:
        return redirect('blog:blog_index') 

    next_url = request.GET.get('next') or request.POST.get('next')
    register_form = RegisterForm(request.POST or None)

    if request.method == 'POST' and register_form.is_valid():
        user = register_form.save()
        login(request, user)

        messages.success(request, _('注册成功，已自动登录。'))

        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        
        return redirect('blog:blog_index')
        
    return render(request, 'blog/register.html', {'form': register_form, 'next': next_url})


def add_blog(request): 
    if not request.user.is_authenticated:
        return redirect('blog:login')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.visitors = 1
            blog.save()
            form.save_m2m()  
            
            # 处理新增标签
            new_tags = request.POST.get('new_tags', '').strip()
            if new_tags:
                tag_names = [t.strip() for t in new_tags.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    blog.tags.add(tag)

            messages.success(request, _('博客发布成功！'))
            return redirect('blog:blog_detail', blog_id=blog.id)
    else:
        form = BlogForm()
    
    return render(request, 'blog/add_blog.html', {'form': form})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('blog:login')
    
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('个人资料更新成功！'))
            return redirect('blog:user_profile', user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile_obj)
    
    user_blogs = Entry.objects.filter(author=request.user).order_by('-created_time')
    
    return render(request, 'blog/profile.html', {
        'form': form,
        'profile_obj': profile_obj,
        'profile_user': request.user,
        'user_blogs': user_blogs,
        'blog_count': user_blogs.count(),
        'is_owner': True,
    })


def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    profile_obj, created = UserProfile.objects.get_or_create(user=profile_user)
    user_blogs = Entry.objects.filter(author=profile_user).order_by('-created_time')

    is_owner = request.user.is_authenticated and request.user == profile_user

    if is_owner and request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('个人资料更新成功！'))
            return redirect('blog:user_profile', user_id=profile_user.id)
    else:
        form = ProfileForm(instance=profile_obj) if is_owner else None

    return render(request, 'blog/profile.html', {
        'profile_obj': profile_obj,
        'profile_user': profile_user,
        'user_blogs': user_blogs,
        'blog_count': user_blogs.count(),
        'is_owner': is_owner,
        'form': form,
    })


def edit_blog(request, blog_id):
    if not request.user.is_authenticated:
        return redirect('blog:login')
    
    blog = get_object_or_404(Entry, id=blog_id)
    
    if blog.author != request.user:
        messages.error(request, _('你没有权限编辑这篇博客！'))
        return redirect('blog:user_profile', user_id=request.user.id)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            
            # 处理新增标签
            new_tags = request.POST.get('new_tags', '').strip()
            if new_tags:
                tag_names = [t.strip() for t in new_tags.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    blog.tags.add(tag)
            
            messages.success(request, _('博客修改成功！'))
            return redirect('blog:blog_detail', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'blog/edit_blog.html', {'form': form, 'blog': blog})


def delete_blog(request, blog_id):
    if not request.user.is_authenticated:
        return redirect('blog:login')
    
    blog = get_object_or_404(Entry, id=blog_id)
    
    if blog.author != request.user:
        messages.error(request, _('你没有权限删除这篇博客！'))
        return redirect('blog:user_profile', user_id=request.user.id)
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, _('博客已删除！'))
        return redirect('blog:user_profile', user_id=request.user.id)
    
    return render(request, 'blog/delete_blog.html', {'blog': blog})



