# Generated by Django 4.1.7 on 2023-02-24 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_coin_identifier_alter_coin_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coin',
            name='identifier',
        ),
        migrations.AlterField(
            model_name='coin',
            name='id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
