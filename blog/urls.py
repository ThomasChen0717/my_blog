from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('<int:blog_id>/', views.detail, name='blog_detail'),
    path('add/', views.add_blog, name='add_blog'),
    path('<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
]
