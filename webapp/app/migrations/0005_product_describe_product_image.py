# Generated by Django 4.2.2 on 2023-07-11 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_quantily_orderitem_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='describe',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]