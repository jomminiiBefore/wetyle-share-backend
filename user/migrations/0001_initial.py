# Generated by Django 3.0.3 on 2020-02-28 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=500)),
                ('kakao_id', models.CharField(max_length=100, null=True)),
                ('facebook_id', models.CharField(max_length=100, null=True)),
                ('twitter_id', models.CharField(max_length=100, null=True)),
                ('google_id', models.CharField(max_length=100, null=True)),
                ('nickname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('image_url', models.URLField(blank=True, max_length=2000, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('website_url', models.URLField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
