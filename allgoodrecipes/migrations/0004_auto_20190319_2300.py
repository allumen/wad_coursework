# Generated by Django 2.1.7 on 2019-03-19 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allgoodrecipes', '0003_auto_20190319_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='preparation_time',
            field=models.IntegerField(default=90),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings_number',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
