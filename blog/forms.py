from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Entry, Category, Tag, UserProfile


class TechClearableFileInput(forms.ClearableFileInput):
    """自定义文件上传组件 - 添加 wrapper class 便于 CSS/JS targeting"""

    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        return mark_safe(
            '<div class="tech-file-input">'
            f'{output}'
            '</div>'
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class BlogForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'blog-category-select'}),
        required=True,
        label=_('分类')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label_from_instance = lambda obj: obj.get_name()

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'blog-tags-select'}),
        required=False,
        label=_('已有标签')
    )
    new_tags = forms.CharField(
        required=False,
        label=_('新增标签'),
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        help_text=_('可以输入新标签')
    )

    class Meta:
        model = Entry
        fields = ('title', 'img', 'body', 'abstract', 'category', 'tags')
        labels = {
            'title': _('标题'),
            'img': _('配图'),
            'body': _('正文'),
            'abstract': _('摘要'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('请输入标题')}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': _('请输入正文')}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('请输入摘要（可选）')}),
            'img': TechClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'birthday', 'gender', 'city', 'occupation', 'bio')
        labels = {
            'avatar': _('头像'),
            'birthday': _('生日'),
            'gender': _('性别'),
            'city': _('城市'),
            'occupation': _('工作'),
            'bio': _('个人简介'),
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.RadioSelect(attrs={'class': 'radio-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('请输入所在城市')}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('请输入职业')}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('介绍一下自己吧')}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
