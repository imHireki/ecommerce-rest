# Generated by Django 3.2.5 on 2021-07-07 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_delete_variacao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='preco_marketing',
            new_name='preco',
        ),
        migrations.RenameField(
            model_name='produto',
            old_name='preco_marketing_promocional',
            new_name='preco_promocional',
        ),
    ]
