# Generated by Django 3.1.7 on 2021-04-02 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20210315_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
