# Generated by Django 3.1 on 2020-08-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='fashion.jpg', height_field='554', upload_to='product_pics', width_field='554'),
        ),
    ]