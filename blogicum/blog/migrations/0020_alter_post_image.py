# Generated by Django 3.2.16 on 2023-07-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_auto_20230725_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='image', verbose_name='Фото'),
        ),
    ]