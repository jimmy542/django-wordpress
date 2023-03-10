# Generated by Django 4.0.5 on 2022-11-26 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wordpress_tag', '0001_initial'),
        ('wordpress_category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordpressPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_name', models.TextField(blank=True)),
                ('wordpress_post_id', models.CharField(default='noid', max_length=100)),
                ('wordpress_website', models.TextField(default='no website')),
                ('detail', models.TextField(default='detail', max_length=100)),
                ('wordpress_content', models.TextField(blank=True)),
                ('wordpress_title', models.TextField(default='notitle', max_length=100)),
                ('active', models.BooleanField(default=False)),
                ('wordpress_status_post', models.TextField(blank=True)),
                ('iframe', models.TextField(default='no iframe')),
                ('focus_keyword', models.TextField(blank=True)),
                ('description_keyword', models.TextField(blank=True)),
                ('category', models.ManyToManyField(default=None, to='wordpress_category.wordpresscategory')),
                ('tag', models.ManyToManyField(default=None, to='wordpress_tag.wordpresstag')),
            ],
        ),
    ]
