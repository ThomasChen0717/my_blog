#!/usr/bin/env bash
# Render build script
# Build Command: ./build.sh
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py compilemessages -l en
python manage.py createsuperuser --noinput || true

# 加载初始数据（分类、标签等），使用 update_or_create 避免冲突
python manage.py shell -c "
from blog.models import Category, Tag

categories = [
    ('读书笔记', 'Reading Notes'),
    ('生活随笔', 'Life Notes'),
    ('学习笔记', 'Study Notes'),
    ('技术分享', 'Tech Sharing'),
    ('项目实战', 'Project Practice'),
    ('原创故事', 'Original Stories'),
]
for name, name_en in categories:
    Category.objects.update_or_create(
        name=name,
        defaults={'name_en': name_en}
    )

tags = ['测试1', '短篇', '日常', '情感']
for name in tags:
    Tag.objects.get_or_create(name=name)

print(f'分类数: {Category.objects.count()}, 标签数: {Tag.objects.count()}')
"