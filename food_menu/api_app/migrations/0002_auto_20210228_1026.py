# Generated by Django 3.1.7 on 2021-02-28 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
