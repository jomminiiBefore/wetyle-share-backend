# Generated by Django 3.0.1 on 2020-03-02 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'collections',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'styles',
            },
        ),
        migrations.CreateModel(
            name='StyleRelatedSellingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Style')),
            ],
            options={
                'db_table': 'style_related_selling_items',
            },
        ),
        migrations.CreateModel(
            name='StyleRelatedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pants', models.CharField(max_length=50)),
                ('skirt', models.CharField(max_length=50)),
                ('shoes', models.CharField(max_length=50)),
                ('bag', models.CharField(max_length=50)),
                ('accessory', models.CharField(max_length=50)),
                ('etc', models.CharField(max_length=50)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='style_related_items', to='card.Style')),
            ],
            options={
                'db_table': 'style_related_items',
            },
        ),
        migrations.CreateModel(
            name='StyleLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Style')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'style_likes',
            },
        ),
        migrations.CreateModel(
            name='StyleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(blank=True, max_length=2000, null=True)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Style')),
            ],
            options={
                'db_table': 'style_images',
            },
        ),
        migrations.CreateModel(
            name='StyleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='card.Style')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='user.User')),
            ],
            options={
                'db_table': 'style_comments',
            },
        ),
        migrations.AddField(
            model_name='style',
            name='style_like',
            field=models.ManyToManyField(through='card.StyleLike', to='user.User'),
        ),
        migrations.AddField(
            model_name='style',
            name='style_related_selling_item',
            field=models.ManyToManyField(through='card.StyleRelatedSellingItem', to='product.Product'),
        ),
        migrations.AddField(
            model_name='style',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='styles', to='user.User'),
        ),
        migrations.CreateModel(
            name='CollectionStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Collection')),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Style')),
            ],
            options={
                'db_table': 'collection_styles',
            },
        ),
        migrations.CreateModel(
            name='CollectionFollower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.Collection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'collection_followers',
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='collection_follower',
            field=models.ManyToManyField(through='card.CollectionFollower', to='user.User'),
        ),
        migrations.AddField(
            model_name='collection',
            name='collection_style',
            field=models.ManyToManyField(through='card.CollectionStyle', to='card.Style'),
        ),
        migrations.AddField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='user.User'),
        ),
    ]
