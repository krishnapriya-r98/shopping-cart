# Generated by Django 4.2.5 on 2024-03-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0005_remove_payment_amount_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
