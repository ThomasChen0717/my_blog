# Generated for nickname field with default value

from django.db import migrations, models


def set_default_nickname(apps, schema_editor):
    """为现有用户设置 nickname = username"""
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('blog', 'UserProfile')
    for user in User.objects.all():
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if not profile.nickname:
            profile.nickname = user.username
            profile.save()


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_category_name_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='昵称'),
        ),
        migrations.RunPython(set_default_nickname, reverse_noop),
    ]
