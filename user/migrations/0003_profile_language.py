# Generated by Django 3.0.7 on 2020-12-15 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201215_1029'),
        ('user', '0002_auto_20201207_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Language'),
        ),
    ]