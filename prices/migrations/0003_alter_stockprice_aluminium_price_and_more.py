# Generated by Django 4.2.5 on 2023-10-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0002_stockprice_delete_aluminiumprice_delete_pvcprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockprice',
            name='aluminium_price',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='stockprice',
            name='pvc_futures_price',
            field=models.CharField(max_length=255),
        ),
    ]
