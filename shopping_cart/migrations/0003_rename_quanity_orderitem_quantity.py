# Generated by Django 4.2.5 on 2024-03-16 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='quanity',
            new_name='quantity',
        ),
    ]
