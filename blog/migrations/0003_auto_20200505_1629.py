# Generated by Django 3.0.5 on 2020-05-05 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_test'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='test',
            new_name='text',
        ),
    ]
