# Generated by Django 4.2.4 on 2023-09-04 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_rename_join_on_author_joined_on_author_picture_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True)),
                ('post', models.ManyToManyField(to='blog_app.post')),
            ],
        ),
    ]
