# Generated by Django 4.2.5 on 2024-03-16 13:50

from django.db import migrations
import shopping_cart.managers


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', shopping_cart.managers.UserManager()),
            ],
        ),
    ]
