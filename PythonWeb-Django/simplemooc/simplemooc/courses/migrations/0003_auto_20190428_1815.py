# Generated by Django 2.2 on 2019-04-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20190428_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='courses/images', verbose_name='Imagem'),
        ),
    ]
